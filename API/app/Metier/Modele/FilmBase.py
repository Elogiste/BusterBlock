class FilmBase:
    def __init__(
        self,
        id: int,
        id_magasin: int,
        titre: str,
        genre: str,
        resume: str,
        nbr_exemplaires_disponible: int,
    ):
        self.id = id
        self.id_magasin = id_magasin
        self.titre = titre
        self.genre = genre
        self.resume = resume
        self.nbr_exemplaires_disponible = nbr_exemplaires_disponible

    # --- id ---
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("L'id du film doit être un entier positif.")
        self._id = value

    # --- id_magasin ---
    @property
    def id_magasin(self):
        return self._id_magasin

    @id_magasin.setter
    def id_magasin(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("L'id du magasin doit être un entier positif.")
        self._id_magasin = value

    # --- titre ---
    @property
    def titre(self):
        return self._titre

    @titre.setter
    def titre(self, value):
        if not value or not value.strip():
            raise ValueError("Le titre du film ne peut pas être vide.")
        self._titre = value.strip()

    # --- genre ---
    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value):
        if not value or not value.strip():
            raise ValueError("Le genre du film ne peut pas être vide.")
        self._genre = value.strip()

    # --- resume ---
    @property
    def resume(self):
        return self._resume

    @resume.setter
    def resume(self, value):
        if value is None:
            self._resume = ""
            return
        if not isinstance(value, str):
            raise ValueError("Le résumé doit être une chaîne.")
        self._resume = value.strip()

    # --- nombre d'exemplaires ---
    @property
    def nbr_exemplaires_disponible(self):
        return self._nbr_exemplaires_disponible

    @nbr_exemplaires_disponible.setter
    def nbr_exemplaires_disponible(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Le nombre d'exemplaires disponibles doit être un entier >= 0.")
        self._nbr_exemplaires_disponible = value

    # --- comparaison ---
    def __eq__(self, other):
        if not isinstance(other, FilmBase):
            return NotImplemented

        return (
            self.id == other.id
            and self.id_magasin == other.id_magasin
            and self.titre == other.titre
            and self.genre == other.genre
            and self.resume == other.resume
            and self.nbr_exemplaires_disponible == other.nbr_exemplaires_disponible
        )
