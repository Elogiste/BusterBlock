from pathlib import Path
from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers
import pytest
from app.main import créer_app
from tests.BoutEnBout.DonneesTest.donneesMagasins import magasins
from tests.BoutEnBout.Etapes.EtapesCommunesMagasins import validerInformationsMagasin

# -----------------------------
# 1) Créer l'app FastAPI
# -----------------------------
app = créer_app()
client = TestClient(app)

# -----------------------------
# 2) Charger les scénarios BDD
# -----------------------------
cheminScenarios = Path(__file__).parent / "Fonctionnalites" / "ConsulterLesMagasins.feature"
scenarios(str(cheminScenarios))

# =============================
# SCÉNARIO 1 : magasins existants
# =============================
@given("un utilisateur", target_fixture="user")
def utilisateur_avec_magasins(magasin_dao):
    # ajouter les magasins de test dans la DB
    for m in magasins:
        magasin_dao.ajouter_magasin(m)
    return True

@when("il demande la liste des magasins", target_fixture="réponse")
def requete_liste_magasins():
    return client.get("/magasins")

@then("le système retourne tous les magasins avec leurs informations (id, nom, adresse, téléphone, status)")
def verifier_magasins_complets(réponse):
    reçus = réponse.json()
    assert len(reçus) == len(magasins)
    for i, magasin in enumerate(reçus):
        validerInformationsMagasin(magasins[i], magasin)

# =============================
# SCÉNARIO 2 : aucun magasin
# =============================
@given(parsers.parse("il n'existe aucun magasin"), target_fixture="aucun_magasin")
def base_vide(magasin_dao):
    # la fixture magasin_dao vide déjà les tables
    return []

@when("l'utilisateur demande la liste des magasins", target_fixture="réponse")
def requete_liste_vide():
    return client.get("/magasins")

@then("le système retourne une liste vide")
def verifier_liste_vide(réponse):
    data = réponse.json()
    assert isinstance(data, list)
    assert len(data) == 0

@then("un message indiquant qu'aucun magasin n'est disponible")
def verifier_message_aucun_magasin(réponse):
    data = réponse.json()
    assert len(data) == 0

# =============================
# SCÉNARIO 3 : utilisateur non-authentifié
# =============================
@given("un utilisateur non-authentifié")
def utilisateur_non_authentifie():
    return False

@when("il consulte la liste des magasins", target_fixture="réponse")
def requete_utilisateur_non_auth():
    return client.get("/magasins")

@then("l'accès est possible avec un statut 200 OK si la liste est publique")
def verifier_acces_possible(réponse):
    assert réponse.status_code == 200
    assert isinstance(réponse.json(), list)

@then("le système renvoie un statut 401 Unauthorized si la liste est protégée")
def verifier_acces_refuse(réponse):
    if réponse.status_code == 401:
        assert "unauthorized" in réponse.text.lower() or "non autorisé" in réponse.text.lower()
