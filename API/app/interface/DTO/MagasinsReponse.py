from app.Interface.DTO.MagasinBaseDTO import MagasinBaseDTO
from pydantic import BaseModel

class MagasinReponse(MagasinBaseDTO):
    id: int
    nom: str
    adresse: str
    telephone: str
    status: bool
    nb_films_disponibles: int = 0
