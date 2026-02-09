import bcrypt
from fastapi import status, HTTPException
from app.Interface.Securite.jwt_utils import AUDIENCE, signer_jwt

class AuthService:
    def __init__(self, dao):
        self.dao = dao

    def vérifier_mot_de_passe(self, clair: str, hashé: str) -> bool:

        clair_bytes = clair.encode("utf-8")
        hash_bytes = hashé.encode("utf-8")

        try:
            return bcrypt.checkpw(clair_bytes, hash_bytes)
        except ValueError:
            return False

    def authentifier(self, courriel, mot_de_passe):

        utilisateur = self.dao.obtenir_utilisateur_par_courriel(courriel)
        if not utilisateur or not self.vérifier_mot_de_passe(mot_de_passe, utilisateur.mot_de_passe):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nom d'utilisateur ou mot de passe invalide")

        roles = self.dao.obtenir_roles(utilisateur.id)

        payload = {
            "sub": utilisateur.id,
            "nom":f"{utilisateur.prenom} {utilisateur.nom}",
            "courriel": utilisateur.courriel,
            f"{AUDIENCE}/roles": roles
        }

        jeton = signer_jwt(payload)
        return jeton

