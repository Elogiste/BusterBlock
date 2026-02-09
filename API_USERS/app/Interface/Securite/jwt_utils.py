from jose import jwt
from jwcrypto import jwk
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Chargement et validation des variables d'environnement
# ---------------------------------------------------------------------------

VARIABLES_REQUISES = [
    "PRIVATE_KEY_PATH",
    "PUBLIC_KEY_PATH",
    "ISSUER",
    "AUDIENCE",
    "KID",
    "ACCESS_TOKEN_EXPIRE_MINUTES"
]

for var in VARIABLES_REQUISES:
    if os.getenv(var) is None:
        raise RuntimeError(f"La variable d'environnement {var} est manquante")

# ---------------------------------------------------------------------------
# Résolution des chemins de fichiers
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent

PRIVATE_KEY_PATH = BASE_DIR / os.getenv("PRIVATE_KEY_PATH")
PUBLIC_KEY_PATH = BASE_DIR / os.getenv("PUBLIC_KEY_PATH")
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    if ACCESS_TOKEN_EXPIRE_MINUTES <= 0:
        raise ValueError()
except ValueError:
    raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES doit être un entier positif.")
ISSUER = os.getenv("ISSUER")
AUDIENCE = os.getenv("AUDIENCE")
ALGORITHM = os.getenv("ALGORITHM", "RS256")
KID = os.getenv("KID")

# Vérification que les fichiers existent
if not PRIVATE_KEY_PATH.exists():
    raise FileNotFoundError(f"Clé privée introuvable : {PRIVATE_KEY_PATH}")

if not PUBLIC_KEY_PATH.exists():
    raise FileNotFoundError(f"Clé publique introuvable : {PUBLIC_KEY_PATH}")

# ---------------------------------------------------------------------------
# Fonctions de lecture des fichiers
# ---------------------------------------------------------------------------

def _lire_fichier(chemin: str) -> bytes:
    with open(chemin, "rb") as f:
        return f.read()

PRIVATE_KEY = _lire_fichier(PRIVATE_KEY_PATH)
PUBLIC_KEY = _lire_fichier(PUBLIC_KEY_PATH)

# ---------------------------------------------------------------------------
# Fonction de génération de JWT
# ---------------------------------------------------------------------------

def signer_jwt(payload: dict) -> str:
    données_jeton = payload.copy()
    maintenant = datetime.now(timezone.utc)
    expire = maintenant + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Claims standards JWT
    données_jeton.update({
        "iat": int(maintenant.timestamp()),
        "exp": expire,
        "iss": ISSUER,
        "aud": AUDIENCE
    })
    
    jeton = jwt.encode(
        données_jeton,
        PRIVATE_KEY,
        algorithm=ALGORITHM,
        headers={"kid": KID}
    )
    return jeton

# ---------------------------------------------------------------------------
# Fonction de génération de JWKS
# ---------------------------------------------------------------------------

def obtenir_jwks_dict():
    public_jwk = jwk.JWK.from_pem(PUBLIC_KEY)
    public_jwk["kid"] = "ma-cle-rsa-1"
    public_jwk["use"] = "sig"
    return {"keys": [public_jwk.export(as_dict=True)]}
