from fastapi.testclient import TestClient
from app.main import app
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from pathlib import Path

client = TestClient(app)

feature_path = Path(__file__).parent / "Fonctionnalites" / "ModifierMagasin.feature"
scenarios(str(feature_path))

# ---------- GIVEN ----------
@given("un manager", target_fixture="headers")
def manager():
    return {"X-User-Role": "manager"}

@given("un utilisateur qui n'est pas manager", target_fixture="headers")
def utilisateur_normal():
    return {"X-User-Role": "user"}

@given("un magasin inexistant", target_fixture="magasin_inexistant")
def magasin_inexistant():
    return 999

# ---------- WHEN ----------
@when("il modifie un magasin avec des informations valides", target_fixture="réponse")
def modifier_magasin_valide(headers):
    payload = {
        "id": 1,
        "nom": "Magasin modifié",
        "adresse": "Nouvelle adresse",
        "telephone": "5145555555",
        "status": True
    }
    return client.put("/magasins/1", json=payload, headers=headers)

@when("il tente de modifier un magasin avec des informations invalides", target_fixture="réponse")
def modifier_magasin_invalide(headers):
    payload = {
        "id": 1,
        "nom": "",
        "adresse": "",
        "telephone": "5145555555",
        "status": True
    }
    return client.put("/magasins/1", json=payload, headers=headers)

@when("il tente de modifier un magasin", target_fixture="réponse")
def modifier_magasin_sans_role(headers):
    payload = {
        "id": 1,
        "nom": "Nom test",
        "adresse": "Adresse test",
        "telephone": "5145555555",
        "status": True
    }
    return client.put("/magasins/1", json=payload, headers=headers)

@when("un manager ou un employé tente de le modifier", target_fixture="réponse")
def modifier_magasin_inexistant(magasin_inexistant):
    headers = {"X-User-Role": "manager"}
    payload = {
        "id": 1,
        "nom": "Nom test",
        "adresse": "Adresse test",
        "telephone": "5145555555",
        "status": True
    }
    return client.put(f"/magasins/{magasin_inexistant}", json=payload, headers=headers)

# ---------- THEN ----------
@then("les modifications sont enregistrées et reflétées dans la liste des magasins")
def verifier_modifications(réponse):
    assert réponse.status_code == 200
    data = réponse.json()
    assert data["resultat"][0]["nom"] == "Magasin modifié"
    assert data["resultat"][0]["status"] is True

@then(parsers.parse("le système refuse la modification avec le code {code:d}"))
def verifier_refus_modification(réponse, code):
    assert réponse.status_code == code

@then(parsers.parse("le système refuse l'opération avec le code {code:d}"))
def verifier_refus_role(réponse, code):
    assert réponse.status_code == code

@then(parsers.parse("le système renvoie le code {code:d}"))
def verifier_magasin_inexistant(réponse, code):
    assert réponse.status_code == code

# ---------- AJOUTS IMPORTÉS DU PREMIER FICHIER ----------
# Ces tests sont logiquement valides pour une modification également.

@then("il renvoie un message d'erreur 400")
def verifier_message_400(réponse):
    assert réponse.status_code == 400

@then(parsers.parse("le code de retour est {code:d}"))
def verifier_code_retour(réponse, code):
    assert réponse.status_code == code

@then(parsers.parse("le système refuse la requête avec le code {code:d}"))
def verifier_requete_refusee(réponse, code):
    assert réponse.status_code == code
