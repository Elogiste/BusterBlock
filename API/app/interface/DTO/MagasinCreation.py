from app.Interface.DTO.MagasinBaseDTO import MagasinBaseDTO

class MagasinCreation(MagasinBaseDTO):
    id: int
    nom: str
    adresse: str
    telephone: str
    status: bool
