from pydantic import BaseModel, field_validator
from typing import Optional

class FilmBaseDTO(BaseModel):
    titre: Optional[str] = None
    genre: Optional[str] = None
    resume: Optional[str] = None
    id_magasin: Optional[int] = None
    nbr_exemplaires_disponible: Optional[int] = None

    @field_validator("titre", check_fields=False)
    @classmethod
    def valider_titre(cls, valeur):
        if valeur is not None and not valeur.strip():
            raise ValueError("Le titre du film ne peut pas être vide.")
        return valeur.strip() if valeur else valeur

    @field_validator("genre", check_fields=False)
    @classmethod
    def valider_genre(cls, valeur):
        if valeur is not None and not valeur.strip():
            raise ValueError("Le genre du film ne peut pas être vide.")
        return valeur.strip() if valeur else valeur

    @field_validator("nbr_exemplaires_disponible", check_fields=False)
    @classmethod
    def valider_nbr_exemplaires(cls, valeur):
        if valeur is not None and valeur < 0:
            raise ValueError("Le nombre d'exemplaires ne peut pas être négatif.")
        return valeur
