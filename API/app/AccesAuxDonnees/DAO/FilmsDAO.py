from typing import List, Optional
import os

from app.AccesAuxDonnees.DAO.BaseDAO import BaseDAO
from app.Metier.Modele.Film import Film


class FilmsDAO(BaseDAO):

    def __init__(self, config: Optional[dict] = None) -> None:
        if config is None:
            config = {
                "host": os.getenv("MARIADB_HOST", "db"),
                "user": os.getenv("MARIADB_USER", "root"),
                "password": os.getenv("MARIADB_PASSWORD", "root"),
                "database": os.getenv("MARIADB_DATABASE", "busterblock_db"),
                "port": int(os.getenv("MARIADB_PORT", 3306)),
            }
        super().__init__(config)

    def _row_vers_film(self, row: dict) -> Film:
        return Film(
            id=row["id"],
            id_magasin=row["id_magasin"],
            titre=row["titre"],
            genre=row["genre"],
            resume=row.get("resume"),
            nbr_exemplaires_disponible=row["nbr_exemplaires_disponible"],
        )


    def lister_films(
        self,
        titre: Optional[str] = None,
        genre: Optional[str] = None,
        disponible: Optional[bool] = None,
    ) -> List[Film]:
        conn = self.get_connexion()
        cur = conn.cursor(dictionary=True)

        try:
            sql = """
                SELECT id, id_magasin, titre, genre, resume, nbr_exemplaires_disponible
                FROM films
                WHERE 1 = 1
            """
            params: list = []

            if titre:
                sql += " AND LOWER(titre) LIKE LOWER(%s)"
                params.append(f"%{titre}%")

            if genre:
                sql += " AND LOWER(genre) = LOWER(%s)"
                params.append(genre)

            if disponible is True:
                sql += " AND nbr_exemplaires_disponible > 0"
            elif disponible is False:
                sql += " AND nbr_exemplaires_disponible = 0"

            cur.execute(sql, tuple(params))
            rows = cur.fetchall()
            return [self._row_vers_film(row) for row in rows]

        finally:
            cur.close()
            conn.close()

    def obtenir_film_par_id(self, id_film: int) -> Optional[Film]:
        conn = self.get_connexion()
        cur = conn.cursor(dictionary=True)

        try:
            cur.execute(
                """
                SELECT id, id_magasin, titre, genre, resume, nbr_exemplaires_disponible
                FROM films
                WHERE id = %s
                """,
                (id_film,),
            )
            row = cur.fetchone()
            if not row:
                return None
            return self._row_vers_film(row)

        finally:
            cur.close()
            conn.close()

    def verifier_disponibilite(self, id_film: int, id_magasin: int) -> bool:
        conn = self.get_connexion()
        cur = conn.cursor(dictionary=True)

        try:
            cur.execute(
                """
                SELECT nbr_exemplaires_disponible
                FROM films
                WHERE id = %s AND id_magasin = %s
                """,
                (id_film, id_magasin),
            )
            row = cur.fetchone()
            if not row:
                return False
            return row["nbr_exemplaires_disponible"] > 0

        finally:
            cur.close()
            conn.close()

    def ajouter_film(
        self,
        id_magasin: int,
        titre: str,
        genre: str,
        resume: Optional[str],
        nbr_exemplaires_disponible: int,
    ) -> Film:
        conn = self.get_connexion()
        cur = conn.cursor(dictionary=True)

        try:
            cur.execute(
                """
                INSERT INTO films (id_magasin, titre, genre, resume, nbr_exemplaires_disponible)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (id_magasin, titre, genre, resume, nbr_exemplaires_disponible),
            )
            conn.commit()
            new_id = cur.lastrowid
            return self.obtenir_film_par_id(new_id)

        finally:
            cur.close()
            conn.close()

    def modifier_disponibilite(
        self,
        id_film: int,
        nbr_exemplaires_disponible: int,
    ) -> Optional[Film]:
        conn = self.get_connexion()
        cur = conn.cursor(dictionary=True)

        try:
            cur.execute(
                """
                UPDATE films
                SET nbr_exemplaires_disponible = %s
                WHERE id = %s
                """,
                (nbr_exemplaires_disponible, id_film),
            )
            conn.commit()


            film = self.obtenir_film_par_id(id_film)
            return film 

        finally:
            cur.close()
            conn.close()

    def modifier_film(
        self,
        id_film: int,
        titre: Optional[str] = None,
        genre: Optional[str] = None,
        resume: Optional[str] = None,
        nbr_exemplaires_disponible: Optional[int] = None,
    ) -> Optional[Film]:
        champs = []
        params: list = []

        if titre is not None:
            champs.append("titre = %s")
            params.append(titre)
        if genre is not None:
            champs.append("genre = %s")
            params.append(genre)
        if resume is not None:
            champs.append("resume = %s")
            params.append(resume)
        if nbr_exemplaires_disponible is not None:
            champs.append("nbr_exemplaires_disponible = %s")
            params.append(nbr_exemplaires_disponible)

        if not champs:
            return self.obtenir_film_par_id(id_film)

        sql = f"UPDATE films SET {', '.join(champs)} WHERE id = %s"
        params.append(id_film)

        conn = self.get_connexion()
        cur = conn.cursor(dictionary=True)

        try:
            cur.execute(sql, tuple(params))
            conn.commit()
            if cur.rowcount == 0:
                return None
            return self.obtenir_film_par_id(id_film)

        finally:
            cur.close()
            conn.close()

    def supprimer_film(self, id_film: int) -> bool:
        conn = self.get_connexion()
        cur = conn.cursor()

        try:
            cur.execute("DELETE FROM films WHERE id = %s", (id_film,))
            conn.commit()
            return cur.rowcount > 0

        finally:
            cur.close()
            conn.close()

