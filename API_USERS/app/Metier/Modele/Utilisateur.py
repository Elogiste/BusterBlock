from typing import List

class Utilisateur:
    def __init__(self, id: int, nom: str, prenom: str, courriel: str, mot_de_passe: str, roles: List[str]):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.courriel = courriel
        self.mot_de_passe = mot_de_passe
        self.roles = roles
