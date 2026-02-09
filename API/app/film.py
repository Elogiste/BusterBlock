from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Film(BaseModel):
    id_media: int = Field(
        ..., 
        description="Identifiant unique du film/média.", 
        json_schema_extra={"example": 1}
    )
    titre: str = Field(
        ..., 
        max_length=100, 
        json_schema_extra={"example": "La guerre des étoiles"}
    )
    genre: str = Field(
        ..., 
        max_length=50, 
        json_schema_extra={"example": "Science-Fiction"}
    )
    resume: Optional[str] = Field(
        None, 
        json_schema_extra={"example": "La bible mais dans l'espace"}
    )
        
    nbr_exemplaire_disponible: int = Field(
        ..., 
        description="Nombre d'exemplaires disponibles pour la location.", 
        json_schema_extra={"example": 5}
    )

    est_disponible_dans_ce_magasin: Optional[bool] = Field(
        None,
        description="Statut de disponibilité dans le magasin spécifié (via id_magasin).",
        json_schema_extra={"example": True}
    )
    
class Config:
    from_attributes = True