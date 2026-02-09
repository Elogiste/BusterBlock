from app.Interface.DTO.FilmBaseDTO import FilmBaseDTO

class FilmCreation(FilmBaseDTO):
    id_magasin: int
    titre: str
    genre: str
    nbr_exemplaires_disponible: int
