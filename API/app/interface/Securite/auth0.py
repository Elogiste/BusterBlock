from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import requests
import os
from typing import List

# --- Variables d'environnement ---
CLE_PUBLIQUE = os.getenv("CLE_PUBLIQUE")
DOMAINE = os.getenv("DOMAINE")
AUDIENCE = os.getenv("AUDIENCE")
ALGORITHMS = ["RS256"]
ISSUER = os.getenv("ISSUER") or f"http://{DOMAINE}"

bearer_scheme = HTTPBearer()

# --- Cache JWKS ---
JWKS_CACHE = None


# ---------------------------------------------------------------------------
# Récupération et mise en cache des clés JWKS
# ---------------------------------------------------------------------------
def obtenir_clé_jwks():
    global JWKS_CACHE
    if JWKS_CACHE is None:
        réponse = requests.get(CLE_PUBLIQUE)
        if réponse.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Impossible de récupérer les clés JWKS"
            )
        JWKS_CACHE = réponse.json()
    return JWKS_CACHE


# ---------------------------------------------------------------------------
# Décodage du jeton JWT + extraction des rôles
# ---------------------------------------------------------------------------
def décoder_jeton(jeton: str):
    jwks = obtenir_clé_jwks()
    en_tete = jwt.get_unverified_header(jeton)

    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == en_tete["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
            break

    if not rsa_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé JWKS introuvable"
        )

    try:
        payload = jwt.decode(
            jeton,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=AUDIENCE,
            issuer=ISSUER
        )

        # -------------------------------------------------------------------
        # Extraction des rôles
        # Auth0 insère les rôles dans un claim personnalisé avec un namespace
        # ex :  "https://monapi.com/roles": ["admin", "gestionnaire"]
        # -------------------------------------------------------------------

        # Claim dynamique basé sur l'audience
        namespace_roles = f"{AUDIENCE}/roles"

        roles = (
            payload.get(namespace_roles) or
            payload.get("roles") or
            payload.get("permissions") or
            []
        )

        # Normaliser en liste
        if not isinstance(roles, list):
            roles = [roles]

        # Ajouter les rôles normalisés dans le payload
        payload["roles"] = roles

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Jeton expiré"
        )
    except jwt.JWTClaimsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Claims du jeton invalides"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Jeton invalide ({str(e)})"
        )


# ---------------------------------------------------------------------------
# Exiger un jeton valide
# ---------------------------------------------------------------------------
def exiger_jeton(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    jeton = credentials.credentials
    return décoder_jeton(jeton)

def require_role(*roles: str):
    """
    Vérifie que l'utilisateur a l'un des rôles autorisés.
    Usage : Depends(require_role("manager", "employe"))
    """
    def role_checker(payload: dict = Depends(exiger_jeton)):
        user_roles: List[str] = payload.get("roles", [])
        if not any(role in user_roles for role in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Accès refusé pour vos rôles: {user_roles}"
            )
        return payload
    return role_checker