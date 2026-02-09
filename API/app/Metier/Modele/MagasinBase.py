from math import isclose

class MagasinBase:
    def __init__(self, id: int, nom: str, adresse: str, telephone: str, status: bool):
        self.id = id
        self.nom = nom
        self.adresse = adresse
        self.telephone = telephone
        self.status = status

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, value):
        if not value or not value.strip():
            raise ValueError("Le nom du magasin ne peut pas être vide.")
        self._nom = value.strip()

    @property
    def adresse(self):
        return self._adresse

    @adresse.setter
    def adresse(self, value):
        if not value or not value.strip():
            raise ValueError("L'adresse du magasin ne peut pas être vide.")
        self._adresse = value.strip()

    @property
    def telephone(self):
        return self._telephone

    @telephone.setter
    def telephone(self, value):
        # Exemple simple : autoriser chiffres, +, -, espaces
        import re
        pattern = r"^[0-9+\- ]{6,}$"
        if not re.match(pattern, value):
            raise ValueError(
                f"Téléphone invalide : {value}. Doit contenir au moins 6 chiffres et seulement chiffres, +, -, espace."
            )
        self._telephone = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, bool):
            self._status = value
        elif isinstance(value, (int, float)):  # accepte 0/1
            self._status = bool(value)
        else:
            raise ValueError("Le status doit être un booléen (True/False).")

    def __eq__(self, other):
        if not isinstance(other, MagasinBase):
            return NotImplemented

        return (
            self.id == other.id
            and self.nom == other.nom
            and self.adresse == other.adresse
            and self.telephone == other.telephone
            and self.status is other.status
        )