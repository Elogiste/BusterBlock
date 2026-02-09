from typing import List, Optional

from app.film import Film
from app.dao.FilmsDao import FilmDAO


class FilmService:

    def __init__(self, dao: Optional[FilmDAO] = None) -> None:
        self._dao = dao or FilmDAO()

    def chercher_films(
        self,
        titre: Optional[str] = None,
        genre: Optional[str] = None,
        disponible: Optional[bool] = None,
    ) -> List[Film]:
        return self._dao.lister_films(
            titre=titre,
            genre=genre,
            disponible=disponible,
        )

    def obtenir_details_film(
        self,
        id_film: int,
        id_magasin: Optional[int] = None,
    ) -> Optional[Film]:
        film = self._dao.obtenir_film_par_id(id_film)
        if not film:
            return None

        film_response = film.model_copy()

        if id_magasin is not None:
            est_disponible = self._dao.verifier_disponibilite(id_film, id_magasin)
            film_response.est_disponible_dans_ce_magasin = est_disponible

        return film_response

    def ajouter_film(
        self,
        id_magasin: int,
        titre: str,
        genre: str,
        resume: Optional[str],
        nbr_exemplaire_disponible: int,
    ) -> Film:

        if not titre or not titre.strip():
            raise ValueError("données invalides")
        if not genre or not genre.strip():
            raise ValueError("données invalides")
        if nbr_exemplaire_disponible is None or nbr_exemplaire_disponible < 0:
            raise ValueError("données invalides")

        return self._dao.ajouter_film(
            id_magasin=id_magasin,
            titre=titre.strip(),
            genre=genre.strip(),
            resume=resume,
            nbr_exemplaire_disponible=nbr_exemplaire_disponible,
        )

    def modifier_disponibilite(
        self,
        id_film: int,
        nbr_exemplaire_disponible: int,
    ) -> Optional[Film]:
        if nbr_exemplaire_disponible is None or nbr_exemplaire_disponible < 0:
            raise ValueError("données invalides")

        return self._dao.modifier_disponibilite(
            id_film=id_film,
            nbr_exemplaire_disponible=nbr_exemplaire_disponible,
        )

    def modifier_film(
        self,
        id_film: int,
        titre: Optional[str] = None,
        genre: Optional[str] = None,
        resume: Optional[str] = None,
        nbr_exemplaire_disponible: Optional[int] = None,
    ) -> Optional[Film]:
        if titre is not None and not titre.strip():
            raise ValueError("données invalides")
        if genre is not None and not genre.strip():
            raise ValueError("données invalides")
        if nbr_exemplaire_disponible is not None and nbr_exemplaire_disponible < 0:
            raise ValueError("données invalides")

        return self._dao.modifier_film(
            id_film=id_film,
            titre=titre.strip() if titre is not None else None,
            genre=genre.strip() if genre is not None else None,
            resume=resume,
            nbr_exemplaire_disponible=nbr_exemplaire_disponible,
        )

    def supprimer_film(self, id_film: int) -> bool:
        return self._dao.supprimer_film(id_film)
