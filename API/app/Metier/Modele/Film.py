from pydantic import BaseModel

class Film(BaseModel):
    id: int
    id_magasin: int
    titre: str
    genre: str
    resume: str
    nbr_exemplaires_disponible: int

    def __eq__(self, other):
        if not isinstance(other, Film):
            return NotImplemented
        return self.id == other.id
