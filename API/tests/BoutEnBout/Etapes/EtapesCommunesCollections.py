from fastapi.testclient import TestClient
from pytest_bdd import given, when, then, parsers
from app.main import app

@then(parsers.parse("Le code de retour est {code:d}"))
def verifierCodeRetour(réponse, code):
    assert réponse.status_code == code

@then(parsers.parse("Le message d'erreur est \"{message}\""))
def verifierMessageErreur(réponse, message):
    données = réponse.json()
    assert message in données.get("detail", "").lower()
    
# Ajouter Magasin
client = TestClient(app)

# --- Fixtures pour les rôles ---
@given("un manager", target_fixture="headers")
def manager():
    return {"X-User-Role": "manager"}

@given("un utilisateur qui n'est pas manager", target_fixture="headers")
def utilisateur_normal():
    return {"X-User-Role": "user"}

# --- Steps pour l'ajout de magasins ---
@when("il ajoute un magasin avec toutes les informations valides", target_fixture="reponse")
def ajouter_magasin_valide(headers):
    payload = {
        "id": 1,
        "nom": "Magasin du Vieux-Port",
        "adresse": "123 Rue St-Paul",
        "telephone": "5141234567",
        "statut": "ouvert"
    }
    return client.post("/magasin/ajouter_un_Magasin", json=payload, headers=headers)

@when("il ajoute un magasin avec des informations manquantes ou invalides", target_fixture="reponse")
def ajouter_magasin_invalide(headers):
    payload = {
        "id": 1,
        "nom": "",
        "adresse": "123 Rue St-Paul",
        "telephone": "5141234567",
        "statut": "ouvert"
    }
    return client.post("/magasin/ajouter_un_Magasin", json=payload, headers=headers)

@when("il tente d'ajouter un magasin", target_fixture="reponse")
def utilisateur_non_manager(headers):
    payload = {
        "id": 1,
        "nom": "Magasin test",
        "adresse": "123 Rue",
        "telephone": "5141234567",
        "statut": "ouvert"
    }
    return client.post("/magasin/ajouter_un_Magasin", json=payload, headers=headers)

# --- Vérifications pour l'ajout ---
@then("le magasin est enregistré")
def verifier_magasin_enregistre(reponse):
    assert reponse.status_code == 201
    data = reponse.json()
    assert data["nom"] == "Magasin du Vieux-Port"
    assert data["adresse"] == "123 Rue St-Paul"
    assert data["telephone"] == "5141234567"
    assert data["statut"] == "ouvert"

@then("le système refuse l'ajout")
def verifier_magasin_refuse(reponse):
    assert reponse.status_code == 400

@then("le système refuse l'opération")
def verifier_role_refuse(reponse):
    assert reponse.status_code == 403

@then("il est visible dans la liste des magasins")
def verifier_visible_liste(reponse):
    assert reponse.status_code == 201