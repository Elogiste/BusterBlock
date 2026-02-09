from app.Interface.DTO.FilmBaseDTO import FilmBaseDTO

class FilmRemplacement(FilmBaseDTO):
    id_magasin: int
    titre: str
    genre: str
    nbr_exemplaires_disponible: int
