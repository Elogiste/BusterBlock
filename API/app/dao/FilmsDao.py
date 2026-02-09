from typing import List, Optional
import os

from app.film import Film
from app.AccesAuxDonnees.DAO.BaseDAO import BaseDAO
from app.AccesAuxDonnees.DAO.FilmsDAO import FilmsDAO


class FilmDAO:

    def __init__(self, config: Optional[dict] = None) -> None:
        self._dao = FilmsDAO(config)

    def _vers_pydantic(self, film_domaine) -> Film:
        return Film(
            id_media=film_domaine.id,
            titre=film_domaine.titre,
            genre=film_domaine.genre,
            resume=film_domaine.resume,
            nbr_exemplaire_disponible=film_domaine.nbr_exemplaires_disponible,
        )

    def _liste_vers_pydantic(self, films_domaine) -> List[Film]:
        return [self._vers_pydantic(f) for f in films_domaine]

    def lister_films(
        self,
        titre: Optional[str] = None,
        genre: Optional[str] = None,
        disponible: Optional[bool] = None,
    ) -> List[Film]:
        films_dom = self._dao.lister_films(
            titre=titre, genre=genre, disponible=disponible
        )
        return self._liste_vers_pydantic(films_dom)

    def obtenir_film_par_id(self, id_film: int) -> Optional[Film]:
        film_dom = self._dao.obtenir_film_par_id(id_film)
        if not film_dom:
            return None
        return self._vers_pydantic(film_dom)

    def verifier_disponibilite(self, id_film: int, id_magasin: int) -> bool:
        return self._dao.verifier_disponibilite(id_film=id_film, id_magasin=id_magasin)

    def ajouter_film(
        self,
        id_magasin: int,
        titre: str,
        genre: str,
        resume: Optional[str],
        nbr_exemplaire_disponible: int,
    ) -> Film:
        film_dom = self._dao.ajouter_film(
            id_magasin=id_magasin,
            titre=titre,
            genre=genre,
            resume=resume,
            nbr_exemplaires_disponible=nbr_exemplaire_disponible,
        )
        return self._vers_pydantic(film_dom)

    def modifier_disponibilite(
        self,
        id_film: int,
        nbr_exemplaire_disponible: int,
    ) -> Optional[Film]:
        film_dom = self._dao.modifier_disponibilite(
            id_film=id_film,
            nbr_exemplaires_disponible=nbr_exemplaire_disponible,
        )
        if not film_dom:
            return None
        return self._vers_pydantic(film_dom)

    def modifier_film(
        self,
        id_film: int,
        titre: Optional[str] = None,
        genre: Optional[str] = None,
        resume: Optional[str] = None,
        nbr_exemplaire_disponible: Optional[int] = None,
    ) -> Optional[Film]:
        film_dom = self._dao.modifier_film(
            id_film=id_film,
            titre=titre,
            genre=genre,
            resume=resume,
            nbr_exemplaires_disponible=nbr_exemplaire_disponible,
        )
        if not film_dom:
            return None
        return self._vers_pydantic(film_dom)

    def supprimer_film(self, id_film: int) -> bool:
        return self._dao.supprimer_film(id_film)

    
