from app.Interface.Securite.jwt_utils import obtenir_jwks_dict
from fastapi import APIRouter, status
from app.Interface.DTO.ConnexionDTO import ConnexionDTO
from app.Interface.DTO.JetonReponse import JetonReponse


class AuthRouteur:
    def __init__(self, service):
        self.service = service
        self.routeur = APIRouter(prefix="/auth", tags=["auth"])
        self._configurer_routes()

    def _configurer_routes(self):
        @self.routeur.post("/connexion", response_model=JetonReponse, status_code=status.HTTP_200_OK)
        def connexion(données: ConnexionDTO):
            jeton = self.service.authentifier(données.courriel, données.mot_de_passe)
            return {"access_token": jeton}
        
        @self.routeur.get("/.well-known/jwks.json")
        def obtenir_jwks():
            return obtenir_jwks_dict()
