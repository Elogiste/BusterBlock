from typing import List
from app.Metier.Modele.MagasinBase import MagasinBase
from app.Metier.Modele.Film import Film

class Magasin(MagasinBase):

    def __init__(self, id: int, nom: str, adresse: str, telephone: str, status: bool, films: List[Film]):
        super().__init__(id, nom, adresse, telephone, status)
        self.films = films

    def __eq__(self, other):
        if not isinstance(other, Magasin):
            return NotImplemented

        return super().__eq__(other) and self.films == other.films
