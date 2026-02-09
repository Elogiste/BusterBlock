from fastapi import Depends, HTTPException, status
from app.Interface.Securite.auth0 import exiger_jeton

def exiger_role(roles_autorises: list[str]):

    def dependency(payload = Depends(exiger_jeton)):
        roles_utilisateur = payload.get("roles", [])
        if not any(r in roles_utilisateur for r in roles_autorises):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès interdit"
            )
        return payload
    return dependency
