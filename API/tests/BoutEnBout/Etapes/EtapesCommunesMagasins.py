import pytest
from pytest_bdd import given, when, then, parsers
from app.main import app
from fastapi.testclient import TestClient
from app.Interface.DTO.MagasinsReponse import MagasinReponse
import pytest
from pytest_bdd import given, then, parsers
from tests.BoutEnBout.DonneesTest.donneesMagasins import magasins


client = TestClient(app)

# Consulter les magasins
# GIVEN
@given("un utilisateur", target_fixture="utilisateur")
def utilisateur_authentifie():
    """Simule un utilisateur authentifié."""
    return {"user": True}


@given("qu il n existe aucun magasin", target_fixture="aucun_magasin")
def aucun_magasin():
    """Simule le cas où aucun magasin n'existe."""
    return True  # Flag pour indiquer l'absence de magasins


@given("un utilisateur non-authentifié", target_fixture="utilisateur_non_auth")
def utilisateur_non_authentifie():
    """Simule un utilisateur non authentifié."""
    return {"user": False}


# WHEN
@when("il demande la liste des magasins", target_fixture="réponse")
def obtenir_liste_magasins(utilisateur=None, utilisateur_non_auth=None, aucun_magasin=None):
    """Appelle l’endpoint pour obtenir la liste des magasins selon le contexte."""
    headers = {}
    if utilisateur and utilisateur.get("user"):
        headers["Authorization"] = "Bearer token-factice"

    # Endpoint simulé pour aucun magasin
    if aucun_magasin:
        response = client.get("/magasins_empty", headers=headers)
    else:
        response = client.get("/magasins", headers=headers)

    return response


# THEN
@then("le système retourne tous les magasins avec leurs informations (id, nom, adresse, téléphone, status)")
def verifier_magasins_complets(réponse):
    """Vérifie que la réponse contient la liste complète des magasins."""
    data = réponse.json()
    assert isinstance(data, list), "La réponse doit être une liste."
    assert len(data) > 0, "La liste des magasins ne doit pas être vide."
    for magasin in data:
        for champ in ["id", "nom", "adresse", "telephone", "status"]:
            assert champ in magasin, f"Le champ '{champ}' est manquant dans la réponse."


@then("le système retourne une liste vide")
def verifier_liste_vide(réponse):
    """Vérifie que la liste retournée est vide."""
    data = réponse.json()
    assert data["magasins"] == [], "La liste des magasins devrait être vide."


@then("un message indiquant qu'aucun magasin n'est disponible")
def verifier_message_absence(réponse):
    """Vérifie que le message d’absence est présent."""
    data = réponse.json()
    assert "aucun magasin" in data["message"].lower(), "Le message attendu est manquant ou incorrect."


@then("l'accès est possible avec un statut 200 OK si la liste est publique")
def verifier_acces_public(réponse):
    """Vérifie qu’un utilisateur non-authentifié peut accéder à la liste publique."""
    assert réponse.status_code in [200, 401], f"Statut inattendu: {réponse.status_code}"
    if réponse.status_code == 200:
        assert isinstance(réponse.json(), list), "Le contenu doit être une liste de magasins si la liste est publique."


@then("le système renvoie un statut 401 Unauthorized si la liste est protégée")
def verifier_refus_acces(réponse):
    """Vérifie que l’accès est refusé à un utilisateur non-authentifié."""
    assert réponse.status_code == 401, f"Le statut devrait être 401, obtenu {réponse.status_code}"

# Rechercher un magasin
# --------------------------
# GIVEN
# --------------------------

@given(parsers.parse("un magasin existant avec l'identifiant {id_magasin:d}"), target_fixture="magasinAttendu")
def documenterMagasin(id_magasin):
    """Retourne un magasin existant à partir des données de test."""
    for magasin in magasins:
        if magasin.id == id_magasin:
            return magasin
    pytest.fail(f"Magasin avec l'id {id_magasin} non trouvé dans les données de test.")


@given(parsers.parse("aucun magasin existant avec l'identifiant {id_magasin:d}"))
def documenterMagasinInexistant(id_magasin):
    """Aucun magasin ne correspond à l'identifiant fourni."""
    pass


# --------------------------
# FONCTION DE VALIDATION
# --------------------------

def validerInformationsMagasin(magasinAttendu, magasinsRecus):
    """Compare les champs importants du magasin attendu et reçu."""
    # si magasinsRecus est une liste, prends le premier
    if isinstance(magasinsRecus, list):
        magasinRecu = magasinsRecus[0]
    else:
        magasinRecu = magasinsRecus

    champs = ["id", "nom", "adresse", "telephone", "status"]
    for champ in champs:
        attendu = getattr(magasinAttendu, champ)
        reçu = magasinRecu.get(champ)
        assert reçu == attendu, f"Différence sur le champ '{champ}': attendu={attendu}, reçu={reçu}"


# --------------------------
# THEN
# --------------------------

@then("la réponse contient les informations du magasin")
def vérifierInformationsMagasin(magasinAttendu, réponse):
    """Vérifie que la réponse contient les informations correctes du magasin."""
    magasinReçu = réponse.json()
    validerInformationsMagasin(magasinAttendu, magasinReçu)


@then("la réponse contient la liste des magasins correspondants")
def vérifierListeMagasins(réponse):
    """Vérifie que la réponse contient une liste de magasins (au moins un)."""
    liste = réponse.json()
    assert isinstance(liste, list), "La réponse devrait être une liste."
    assert len(liste) > 0, "Aucun magasin n'a été trouvé alors qu'il devrait y en avoir au moins un."


@then("la réponse contient une liste vide et un message d'absence de résultat")
def vérifierListeVideEtMessage(réponse):
    """Vérifie que le système indique qu'aucun magasin ne correspond."""
    corps = réponse.json()
    assert corps["magasins"] == [], "La liste des magasins devrait être vide."
    assert "aucun magasin" in corps["message"].lower(), "Le message d'erreur attendu est manquant ou incorrect."

# Ajouter Magssin
# --- Steps pour la suppression de magasins ---
@when("il supprime un magasin", target_fixture="reponse")
def supprimer_magasin_valide(headers):
    magasin_id = 1
    return client.delete(f"/magasin/{magasin_id}", headers=headers)

@when("il tente de supprimer un magasin lié à un inventaire actif", target_fixture="reponse")
def supprimer_magasin_actif(headers):
    magasin_id = 2
    return client.delete(f"/magasin/{magasin_id}", headers=headers)

@when("il tente de supprimer un magasin", target_fixture="reponse")
def supprimer_magasin_non_manager(headers):
    magasin_id = 1
    return client.delete(f"/magasin/{magasin_id}", headers=headers)

@when("il tente de supprimer un magasin inexistant", target_fixture="reponse")
def supprimer_magasin_inexistant(headers):
    magasin_id = 9999
    return client.delete(f"/magasin/{magasin_id}", headers=headers)

# --- Vérifications pour la suppression ---
@then("celui-ci est retiré de la liste publique")
def verifier_magasin_supprime(reponse):
    assert reponse.status_code == 200

@then("le système refuse l'opération")
def verifier_operation_refuse(reponse):
    assert reponse.status_code in (403, 409)

@then("le code de retour est 200")
def verifier_code_200(reponse):
    assert reponse.status_code == 200

@then("le code de retour est 403")
def verifier_code_403(reponse):
    assert reponse.status_code == 403

@then("le code de retour est 409")
def verifier_code_409(reponse):
    assert reponse.status_code == 409

@then("le système renvoie 404")
def verifier_code_404(reponse):
    assert reponse.status_code == 404