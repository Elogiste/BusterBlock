from fastapi import APIRouter, Query, HTTPException, status, Path, Depends
from typing import List, Optional
from pydantic import BaseModel

from app.film import Film
from app.dao.FilmsDao import FilmDAO
from app.Metier.Services.FilmsService import FilmService

# 🔐 Auth0 role checker (même style que MagasinsRouteur)
from app.Interface.Securite.auth0 import require_role

router = APIRouter(prefix="/films", tags=["films"])

film_dao = FilmDAO()
film_service = FilmService(dao=film_dao)


# -----------------------------------------------
#   DTO
# -----------------------------------------------
class FilmCreation(BaseModel):
    id_magasin: int
    titre: str
    genre: str
    resume: Optional[str]
    nbr_exemplaire_disponible: int


class FilmModification(BaseModel):
    titre: Optional[str]
    genre: Optional[str]
    resume: Optional[str]
    nbr_exemplaire_disponible: Optional[int]


class DisponibiliteModification(BaseModel):
    nbr_exemplaire_disponible: int


# -----------------------------------------------
#   ROUTES
# -----------------------------------------------

# ---- GET /films (ouvert à tous les rôles)
@router.get("/", response_model=List[Film])
async def chercher_films(
    titre: Optional[str] = Query(None),
    genre: Optional[str] = Query(None),
    disponible: Optional[bool] = Query(None),
    user: dict = Depends(require_role("visiteur", "membre", "employe", "manager"))
):
    return film_service.chercher_films(titre=titre, genre=genre, disponible=disponible)


# ---- GET /films/details/{id_film}
@router.get("/details/{id_film}", response_model=Film, status_code=200)
async def consulter_details_film(
    id_film: int = Path(...),
    id_magasin: Optional[int] = Query(None),
    user: dict = Depends(require_role("visiteur", "membre", "employe", "manager"))
):
    film = film_service.obtenir_details_film(id_film=id_film, id_magasin=id_magasin)
    if film is None:
        raise HTTPException(404, f"Film avec ID {id_film} non trouvé")
    return film


# ---- POST /films (réservé manager)
@router.post("/", response_model=Film, status_code=201)
async def ajouter_film(
    payload: FilmCreation,
    user: dict = Depends(require_role("manager"))
):
    try:
        return film_service.ajouter_film(
            id_magasin=payload.id_magasin,
            titre=payload.titre,
            genre=payload.genre,
            resume=payload.resume,
            nbr_exemplaire_disponible=payload.nbr_exemplaire_disponible,
        )
    except ValueError:
        raise HTTPException(400, "Données invalides")


# ---- PUT /films/{id_film} (manager)
@router.put("/{id_film}", response_model=Film)
async def modifier_film(
    id_film: int,
    payload: FilmModification,
    user: dict = Depends(require_role("manager"))
):
    film = film_service.modifier_film(
        id_film=id_film,
        titre=payload.titre,
        genre=payload.genre,
        resume=payload.resume,
        nbr_exemplaire_disponible=payload.nbr_exemplaire_disponible,
    )
    if film is None:
        raise HTTPException(404, f"Film {id_film} non trouvé")
    return film


# ---- DELETE /films/{id_film} (manager)
@router.delete("/{id_film}", status_code=200)
async def supprimer_film(
    id_film: int,
    user: dict = Depends(require_role("manager"))
):
    if not film_service.supprimer_film(id_film):
        raise HTTPException(404, f"Film {id_film} non trouvé")
    return {"message": f"Film {id_film} supprimé."}


# ---- PATCH /films/{id_film}/disponibilite (employé + manager)
@router.patch("/{id_film}/disponibilite", response_model=Film)
async def modifier_disponibilite(
    id_film: int,
    payload: DisponibiliteModification,
    user: dict = Depends(require_role("employe", "manager"))
):
    film = film_service.modifier_disponibilite(
        id_film=id_film,
        nbr_exemplaire_disponible=payload.nbr_exemplaire_disponible,
    )
    if film is None:
        raise HTTPException(404, f"Film {id_film} non trouvé")
    return film
