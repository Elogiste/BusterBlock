from app.Interface.DTO.MagasinBaseDTO import MagasinBaseDTO
from typing import Optional

class MagasinModification(MagasinBaseDTO):
    nom: Optional[str] = None
    adresse: Optional[str] = None
    telephone: Optional[str] = None
    status: Optional[bool] = None
