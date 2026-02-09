from typing import List
from fastapi import HTTPException, status
from app.Metier.Modele.Magasin import Magasin
from app.AccesAuxDonnees.DAO.MagasinsDAO import MagasinsDAO
from app.Interface.DTO.MagasinCreation import MagasinCreation
from app.Interface.DTO.MagasinModification import MagasinModification
from app.Interface.DTO.MagasinRemplacement import MagasinRemplacement
from app.Interface.DTO.MagasinsReponse import MagasinReponse

class MagasinsService:
    def __init__(self, dao: MagasinsDAO):
        self.dao = dao

    # Conversion Magasin -> MagasinReponse
    def convertir_magasin_en_reponse(self, magasin: Magasin) -> MagasinReponse:
        return MagasinReponse(
            id=magasin.id,
            nom=magasin.nom,
            adresse=magasin.adresse,
            telephone=magasin.telephone,
            status=magasin.status,
            nb_films_disponibles=len(getattr(magasin, "films", []))
        )

    # Lister tous les magasins
    def obtenir_tous_les_magasins(self) -> List[MagasinReponse]:
        magasins = self.dao.obtenir_tous_les_magasins()
        return [self.convertir_magasin_en_reponse(m) for m in magasins]

    # Obtenir un magasin par ID
    def obtenir_magasin_par_id(self, magasin_id: int) -> MagasinReponse:
        magasin = self.dao.obtenir_magasin_par_id(magasin_id)
        if not magasin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Magasin {magasin_id} inexistant")
        return self.convertir_magasin_en_reponse(magasin)

    # Rechercher magasins par nom
    def chercher_magasin_par_nom(self, nom: str) -> List[MagasinReponse]:
        magasins = self.dao.chercher_magasin_par_nom(nom)
        return [self.convertir_magasin_en_reponse(m) for m in magasins]

    # Ajouter un magasin
    def créer_magasin(self, magasin_dto: MagasinCreation) -> MagasinReponse:
        # On ajoute films=[] pour éviter l'erreur
        magasin = Magasin(**magasin_dto.model_dump(), films=[])  

        if self.dao.obtenir_magasin_par_id(magasin.id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Un magasin avec l'ID {magasin.id} existe déjà"
            )

        if self.dao.obtenir_magasin_par_nom(magasin.nom):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Un magasin avec le nom '{magasin.nom}' existe déjà"
            )

        nouveau = self.dao.ajouter_magasin(magasin)

        if not nouveau:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erreur lors de la création du magasin"
            )

        return self.convertir_magasin_en_reponse(nouveau)

    # Remplacer ou créer un magasin
    def remplacer_magasin(self, magasin_id: int, magasin_dto: MagasinRemplacement) -> tuple[MagasinReponse, bool]:
        magasin = Magasin(**magasin_dto.model_dump())
        magasin.id = magasin_id
        existant = self.dao.obtenir_magasin_par_id(magasin_id)
        if existant:
            resultat = self.dao.remplacer(magasin)
            if not resultat:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur lors du remplacement du magasin {magasin_id}")
            return self.convertir_magasin_en_reponse(resultat), False  # False = pas créé
        else:
            return self.créer_magasin(magasin), True  # True = créé

    # Modifier partiellement un magasin
    def modifier_magasin(self, magasin_id: int, modifs_dto: MagasinModification) -> MagasinReponse:
        magasin = self.dao.obtenir_magasin_par_id(magasin_id)
        if not magasin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Magasin {magasin_id} inexistant")
        modifs = modifs_dto.model_dump(exclude_unset=True)
        for champ, valeur in modifs.items():
            setattr(magasin, champ, valeur)
        resultat = self.dao.remplacer(magasin)
        if not resultat:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur lors de la modification du magasin {magasin_id}")
        return self.convertir_magasin_en_reponse(resultat)

    # Supprimer un magasin
    def supprimer_magasin(self, magasin_id: int) -> None:
        magasin = self.dao.obtenir_magasin_par_id(magasin_id)
        if not magasin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Magasin {magasin_id} inexistant")
        if not self.dao.supprimer(magasin_id):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur lors de la suppression du magasin {magasin_id}")
