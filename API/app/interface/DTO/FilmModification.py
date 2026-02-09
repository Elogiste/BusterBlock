from app.Interface.DTO.FilmBaseDTO import FilmBaseDTO
from typing import Optional

class FilmModification(FilmBaseDTO):
    titre: Optional[str] = None
    genre: Optional[str] = None
    resume: Optional[str] = None
    id_magasin: Optional[int] = None
    nbr_exemplaires_disponible: Optional[int] = None
