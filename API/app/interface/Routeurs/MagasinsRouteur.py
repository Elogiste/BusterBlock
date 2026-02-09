from fastapi import APIRouter, status, Response, Query, Depends
from typing import List, Optional
from app.Metier.Services.MagasinsService import MagasinsService
from app.Interface.DTO.MagasinCreation import MagasinCreation
from app.Interface.DTO.MagasinModification import MagasinModification
from app.Interface.DTO.MagasinRemplacement import MagasinRemplacement
from app.Interface.DTO.MagasinsReponse import MagasinReponse
from app.Interface.Securite.auth0 import require_role


class MagasinsRouteur:
    def __init__(self, service: MagasinsService):
        self.service = service
        self.routeur = APIRouter(prefix="/magasins", tags=["magasins"])
        self._configurer_routes()

    def _configurer_routes(self):

        @self.routeur.get("/{magasin_id}", response_model=MagasinReponse)
        def obtenir_magasin_par_id(magasin_id: int, user: dict = Depends(require_role("visiteur", "membre", "employe", "manager"))) -> MagasinReponse:
            return self.service.obtenir_magasin_par_id(magasin_id)

        @self.routeur.get("", response_model=List[MagasinReponse])
        def obtenir_magasins(nom: Optional[str] = Query(None, description="Nom complet ou partiel du magasin"), user: dict = Depends(require_role("visiteur", "membre", "employe", "manager"))) -> List[MagasinReponse]:
            if nom:
                return self.service.chercher_magasin_par_nom(nom)
            return self.service.obtenir_tous_les_magasins()

        @self.routeur.post("", response_model=MagasinReponse, status_code=status.HTTP_201_CREATED)
        def creer_magasin(magasin: MagasinCreation, user: dict = Depends(require_role("manager"))) -> MagasinReponse:
            return self.service.créer_magasin(magasin)

        @self.routeur.put("/{magasin_id}", response_model=MagasinReponse)
        def remplacer_magasin(magasin_id: int, magasin: MagasinRemplacement, réponse: Response, user: dict = Depends(require_role("manager"))) -> MagasinReponse:
            magasin_réponse, créé = self.service.remplacer_magasin(magasin_id, magasin)
            réponse.status_code = status.HTTP_201_CREATED if créé else status.HTTP_200_OK
            return magasin_réponse

        @self.routeur.patch("/{magasin_id}", response_model=MagasinReponse)
        def modifier_magasin(magasin_id: int, modifs: MagasinModification, user: dict = Depends(require_role("manager", "employe"))) -> MagasinReponse:
            return self.service.modifier_magasin(magasin_id, modifs)

        @self.routeur.delete("/{magasin_id}", status_code=status.HTTP_204_NO_CONTENT)
        def supprimer_magasin(magasin_id: int, user: dict = Depends(require_role("manager"))) -> None:
            self.service.supprimer_magasin(magasin_id)
            
