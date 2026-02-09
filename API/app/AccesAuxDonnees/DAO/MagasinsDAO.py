from typing import List, Optional
import unicodedata
from app.Metier.Modele.Magasin import Magasin
from app.Metier.Modele.Film import Film
from app.AccesAuxDonnees.DAO.BaseDAO import BaseDAO


class MagasinsDAO(BaseDAO):

    def __init__(self, config):
        super().__init__(config)

    def convertir_enregistrement_en_magasin(self, enregistrements) -> List[Magasin]:
        magasins_dict = {}

        for enregistrement in enregistrements:
            magasin_id = enregistrement["id_magasin"] 
            if magasin_id not in magasins_dict:
                magasins_dict[magasin_id] = Magasin(
                    id=magasin_id,
                    nom=enregistrement["nom_magasin"],
                    adresse=enregistrement["adresse"],
                    telephone=enregistrement["telephone"],
                    status=bool(enregistrement["status"]),
                    films=[]
                )
            # Ajout du film complet si présent
            if "id_film" in enregistrement and enregistrement["id_film"] is not None:
                magasins_dict[magasin_id].films.append(Film(
                    id=enregistrement["id_film"],
                    id_magasin=magasin_id,
                    titre=enregistrement["titre"],
                    genre=enregistrement["genre"],
                    resume=enregistrement["resume"],
                    nbr_exemplaires_disponible=enregistrement["nbr_exemplaires_disponible"]
                ))

        return list(magasins_dict.values())

    # ------------------ Magasins ------------------

    def obtenir_tous_les_magasins(self) -> List[Magasin]:
        conn = self.get_connexion()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("""
                SELECT 
                    m.id AS id_magasin, m.nom AS nom_magasin, m.adresse, m.telephone, m.status,
                    f.id AS id_film, f.titre, f.genre, f.resume, f.nbr_exemplaires_disponible
                FROM magasins m
                LEFT JOIN films f ON f.id_magasin = m.id
                ORDER BY m.id
            """)
            enregistrements = cur.fetchall()
            return self.convertir_enregistrement_en_magasin(enregistrements)
        finally:
            cur.close()
            conn.close()

    def obtenir_magasin_par_id(self, magasin_id: int) -> Optional[Magasin]:
        conn = self.get_connexion()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("""
                SELECT 
                    m.id AS id_magasin, m.nom AS nom_magasin, m.adresse, m.telephone, m.status,
                    f.id AS id_film, f.titre, f.genre, f.resume, f.nbr_exemplaires_disponible
                FROM magasins m
                LEFT JOIN films f ON f.id_magasin = m.id
                WHERE m.id = %s
            """, (magasin_id,))
            enregistrements = cur.fetchall()
            magasins = self.convertir_enregistrement_en_magasin(enregistrements)
            return magasins[0] if magasins else None
        finally:
            cur.close()
            conn.close()

    def obtenir_magasin_par_nom(self, nom: str) -> Optional[Magasin]:
        conn = self.get_connexion()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("""
                SELECT 
                    m.id AS id_magasin, m.nom AS nom_magasin, m.adresse, m.telephone, m.status,
                    f.id AS id_film, f.titre, f.genre, f.resume, f.nbr_exemplaires_disponible
                FROM magasins m
                LEFT JOIN films f ON f.id_magasin = m.id
                WHERE LOWER(m.nom) = LOWER(%s)
            """, (nom,))
            enregistrements = cur.fetchall()
            magasins = self.convertir_enregistrement_en_magasin(enregistrements)
            return magasins[0] if magasins else None
        finally:
            cur.close()
            conn.close()

    def chercher_magasin_par_nom(self, nom: str) -> List[Magasin]:
        nom = (nom or "").strip()
        nom = unicodedata.normalize("NFC", nom)
        if not nom:
            return []

        pattern = f"%{nom}%"
        conn = self.get_connexion()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("""
                SELECT 
                    m.id AS id_magasin, m.nom AS nom_magasin, m.adresse, m.telephone, m.status,
                    f.id AS id_film, f.titre, f.genre, f.resume, f.nbr_exemplaires_disponible
                FROM magasins m
                LEFT JOIN films f ON f.id_magasin = m.id
                WHERE LOWER(m.nom) LIKE LOWER(%s)
            """, (pattern,))
            enregistrements = cur.fetchall()
            return self.convertir_enregistrement_en_magasin(enregistrements)
        finally:
            cur.close()
            conn.close()

    def ajouter_magasin(self, magasin: Magasin) -> Optional[Magasin]:
        conn = self.get_connexion()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO magasins (id, nom, adresse, telephone, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (magasin.id, magasin.nom, magasin.adresse, magasin.telephone, magasin.status))
            conn.commit()
            return self.obtenir_magasin_par_id(magasin.id)
        except Exception as e:
            conn.rollback()
            print(f"Erreur lors de la création d'un magasin: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    def supprimer(self, magasin_id: int) -> bool:
        conn = self.get_connexion()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM magasins WHERE id = %s", (magasin_id,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Erreur lors de la suppression du magasin {magasin_id}: {e}")
            return False
        finally:
            cur.close()
            conn.close()

    def remplacer(self, magasin: Magasin) -> Optional[Magasin]:
        conn = self.get_connexion()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE magasins
                SET nom = %s, adresse = %s, telephone = %s, status = %s
                WHERE id = %s
            """, (magasin.nom, magasin.adresse, magasin.telephone, magasin.status, magasin.id))
            conn.commit()
            return self.obtenir_magasin_par_id(magasin.id)
        except Exception as e:
            conn.rollback()
            print(f"Erreur lors du remplacement du magasin {magasin.id}: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    # ------------------ Films dans magasin ------------------

    def ajouter_film_au_magasin(self, magasin_id: int, film_id: int, quantite: int, disponible: bool):
        if quantite < 0:
            raise ValueError("Quantité invalide")
        conn = self.get_connexion()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO inventaire (id_magasin, id_film, quantite, disponible)
                VALUES (%s, %s, %s, %s)
            """, (magasin_id, film_id, quantite, disponible))
            conn.commit()
        finally:
            cur.close()
            conn.close()

    def modifier_film_du_magasin(self, magasin_id: int, film_id: int, quantite=None, disponible=None):
        conn = self.get_connexion()
        cur = conn.cursor()
        try:
            champs = []
            valeurs = []
            if quantite is not None:
                champs.append("quantite=%s")
                valeurs.append(quantite)
            if disponible is not None:
                champs.append("disponible=%s")
                valeurs.append(disponible)
            valeurs += [magasin_id, film_id]
            cur.execute(f"""
                UPDATE inventaire
                SET {', '.join(champs)}
                WHERE id_magasin=%s AND id_film=%s
            """, valeurs)
            conn.commit()
        finally:
            cur.close()
            conn.close()

    def lister_inventaire(self, magasin_id=None):
        conn = self.get_connexion()
        cur = conn.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM inventaire"
            if magasin_id:
                sql += " WHERE id_magasin=%s"
                cur.execute(sql, (magasin_id,))
            else:
                cur.execute(sql)
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

    def magasins_avec_film_disponible(self, film_id: int) -> list[dict]:
        conn = self.get_connexion()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("""
                SELECT m.id AS magasin_id, m.nom, m.adresse, i.quantite AS quantite_disponible
                FROM magasins m
                JOIN inventaire i ON i.id_magasin = m.id
                WHERE i.id_film = %s AND i.disponible = TRUE AND i.quantite > 0
            """, (film_id,))
            return cur.fetchall()
        except Exception as e:
            print(f"Erreur lors de l'obtention des magasins pour le film {film_id}: {e}")
            return []
        finally:
            cur.close()
            conn.close()

    def film_existe(self, film_id: int) -> bool:
        conn = self.get_connexion()
        cur = conn.cursor()
        try:
            cur.execute("SELECT 1 FROM films WHERE id = %s", (film_id,))
            return cur.fetchone() is not None
        finally:
            cur.close()
            conn.close()

