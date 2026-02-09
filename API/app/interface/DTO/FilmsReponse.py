from app.Interface.DTO.FilmBaseDTO import FilmBaseDTO

class FilmReponse(FilmBaseDTO):
    id: int
    id_magasin: int
    titre: str
    genre: str
    nbr_exemplaires_disponible: int
    est_disponible: bool | None = None
