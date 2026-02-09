from app.Interface.DTO.MagasinBaseDTO import MagasinBaseDTO

class MagasinRemplacement(MagasinBaseDTO):
    nom: str
    adresse: str
    telephone: str
    status: bool
