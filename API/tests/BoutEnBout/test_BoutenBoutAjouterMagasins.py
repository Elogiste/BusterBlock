from fastapi.testclient import TestClient
import pytest
from app.main import app
from pytest_bdd import scenarios, given, when, then, parsers
from pathlib import Path

client = TestClient(app)

cheminScenarios = Path(__file__).parent / "Fonctionnalites" / "AjouterMagasin.feature"
scenarios(str(cheminScenarios))

# ---------- GIVEN ----------
@given("un manager", target_fixture="headers")
def manager():
    return {"X-User-Role": "manager"}

@given("un utilisateur qui n'est pas manager", target_fixture="headers")
def utilisateur_normal():
    return {"X-User-Role": "user"}

# ---------- WHEN ----------
@when("il ajoute un nouveau magasin avec toutes les informations valides", target_fixture="réponse")
@when("il ajoute un nouveau magasin avec des informations valides", target_fixture="réponse")
def ajouter_magasin_valide(headers):
    payload = {
        "id": 11,
        "nom": "Magasin du Vieux-Port",
        "adresse": "123 Rue St-Paul",
        "telephone": "5141234567",
        "status": True
    }
    return client.post("/magasins", json=payload, headers=headers)

@when("il ajoute un magasin avec des informations manquantes ou invalides", target_fixture="réponse")
def ajouter_magasin_invalide(headers):
    payload = {
        "id": 12,
        "nom": "",
        "adresse": "123 Rue St-Paul",
        "telephone": "5141234567",
        "status": True
    }
    return client.post("/magasins", json=payload, headers=headers)

@when("il tente d'ajouter un nouveau magasin", target_fixture="réponse")
def utilisateur_non_manager(headers):
    payload = {
        "id": 13,
        "nom": "Magasin test",
        "adresse": "123 Rue",
        "telephone": "5141234567",
        "status": True
    }
    return client.post("/magasins", json=payload, headers=headers)

# ---------- THEN ----------
@then("le magasin est enregistré")
def verifier_magasin_enregistre(réponse):
    assert réponse.status_code == 201
    data = réponse.json()
    #data.get("nom") renvoie None parce que le champ nom n’est pas au premier niveau, il est dans data["resultat"][0]["nom"]
    # accéder au premier élément de la liste "resultat"
    magasin = data["resultat"][0]
    assert magasin["nom"] == "Magasin du Vieux-Port"
    assert magasin["adresse"] == "123 Rue St-Paul"
    assert magasin["telephone"] == "5141234567"
    assert magasin["status"] is True

@then(parsers.parse("le système refuse la requête avec le code {code:d}"))
def verifier_magasin_refuse(réponse, code):
    assert réponse.status_code == code

@then(parsers.parse("le système refuse l'opération avec le code {code:d}"))
def verifier_role_refuse(réponse, code):
    assert réponse.status_code == code

@then("il est visible dans la liste des magasins")
def verifier_visible_liste(réponse):
    assert réponse.status_code == 201

@then(parsers.parse("le code de retour est {code:d}"))
def verifier_code(réponse, code):
    assert réponse.status_code == code

@then("il renvoie un message d'erreur 400")
def verifier_message_400(réponse):
    assert réponse.status_code == 400

# ---------- AJOUT DU TEST MANQUANT ----------
@then(parsers.parse("le système renvoie le code {code:d}"))
def verifier_code_systeme(réponse, code):
    assert réponse.status_code == code
