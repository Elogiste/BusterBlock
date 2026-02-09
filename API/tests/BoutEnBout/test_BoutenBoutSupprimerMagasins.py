from fastapi.testclient import TestClient
import pytest
from app.main import app
from pytest_bdd import scenarios, given, when, then, parsers
from pathlib import Path

client = TestClient(app)

chemin_scenarios = Path(__file__).parent / "Fonctionnalites" / "SupprimerMagasin.feature"
scenarios(str(chemin_scenarios))

# ---------- GIVEN ----------
@given("un manager", target_fixture="headers")
def manager():
    return {"X-User-Role": "manager"}

@given("un utilisateur qui n'est pas manager", target_fixture="headers")
def utilisateur_normal():
    return {"X-User-Role": "user"}

# ---------- WHEN ----------
@when("il supprime un magasin existant", target_fixture="réponse")
@when("Lorsqu'il supprime un magasin existant", target_fixture="réponse")
def supprimer_magasin_valide(headers):
    return client.delete("/magasins/1", headers=headers)

@when("il tente de supprimer un magasin lié à un inventaire actif", target_fixture="réponse")
@when("Lorsqu'il tente de supprimer un magasin lié à un inventaire actif", target_fixture="réponse")
def supprimer_magasin_actif(headers):
    return client.delete("/magasins/2", headers=headers)

@when("il tente de supprimer un magasin sans rôle manager", target_fixture="réponse")
@when("Lorsqu'il tente de supprimer un magasin sans rôle manager", target_fixture="réponse")
def supprimer_magasin_non_manager(headers):
    return client.delete("/magasins/1", headers=headers)

@when("il tente de supprimer un magasin inexistant", target_fixture="réponse")
@when("Lorsqu'il tente de supprimer un magasin inexistant", target_fixture="réponse")
def supprimer_magasin_inexistant(headers):
    return client.delete("/magasins/9999", headers=headers)

# ---------- THEN ----------
@then("le magasin est retiré de la liste publique")
@then("Alors le magasin est retiré de la liste publique")
def verifier_magasin_supprime(réponse):
    assert réponse.status_code == 200

@then("le système refuse l'opération avec le code 403")
def verifier_refus_403(réponse):
    assert réponse.status_code == 403

@then("le système refuse l'opération avec le code 409")
def verifier_refus_409(réponse):
    assert réponse.status_code == 409

@then("le système renvoie le code 404")
def verifier_code_404(réponse):
    assert réponse.status_code == 404

@then("le code de retour est 200")
def verifier_code_200(réponse):
    assert réponse.status_code == 200

# ---------- AJOUTS IMPORTÉS DU PREMIER FICHIER ----------
# Les tests génériques suivants sont pertinents aussi pour la suppression.

@then(parsers.parse("le système renvoie le code {code:d}"))
def verifier_code_generique(réponse, code):
    assert réponse.status_code == code

@then(parsers.parse("le système refuse la requête avec le code {code:d}"))
def verifier_requete_refusee_generique(réponse, code):
    assert réponse.status_code == code

@then(parsers.parse("le système refuse l'opération avec le code {code:d}"))
def verifier_operation_refuse_generique(réponse, code):
    assert réponse.status_code == code
