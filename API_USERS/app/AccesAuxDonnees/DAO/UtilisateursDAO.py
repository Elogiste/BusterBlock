from typing import List, Optional
from app.AccesAuxDonnees.DAO.BaseDAO import BaseDAO
from app.Metier.Modele.Utilisateur import Utilisateur

class UtilisateursDAO(BaseDAO):

    def __init__(self, config):
        super().__init__(config)

    def convertir_enregistrement_en_utilisateur(self, enregistrements) -> List[Utilisateur]:
        utilisateurs_dict = {}
        for enregistrement in enregistrements:
            utilisateur_id = enregistrement["id"]
            if utilisateur_id not in utilisateurs_dict:
                utilisateurs_dict[utilisateur_id] = Utilisateur(
                    id=utilisateur_id,
                    nom=enregistrement["nom"],
                    prenom=enregistrement["prenom"],
                    courriel=enregistrement["courriel"],
                    mot_de_passe=enregistrement["mot_de_passe"],
                    roles=[]
                )

        return list(utilisateurs_dict.values())

    def obtenir_utilisateur_par_courriel(self, courriel: str) -> Optional[Utilisateur]:
        conn = self.get_connexion()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("""
                SELECT id, nom, prenom, courriel, mot_de_passe
                FROM utilisateurs
                WHERE LOWER(courriel) = LOWER(%s)
            """, (courriel,))
            enregistrements = cur.fetchall()
            utilisateurs = self.convertir_enregistrement_en_utilisateur(enregistrements)
            return utilisateurs[0] if utilisateurs else None
        
        except Exception as e:
            print(f"Erreur lors de l'obtention de l'utilisateurs {courriel}: {e}")
            return None
        
        finally:
            cur.close()
            conn.close()

    def obtenir_roles(self, utilisateur_id: int):
        conn = self.get_connexion()
        cur = conn.cursor(dictionary=True)

        try:
            cur = conn.cursor()
            cur.execute(
            "SELECT r.nom FROM roles r JOIN utilisateurs_roles ur ON r.id = ur.role_id WHERE ur.utilisateur_id = %s",
            (utilisateur_id,)
            )
            return [enregistrement[0] for enregistrement in cur.fetchall()]
        
        finally:
            cur.close()
            conn.close()
