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
cheminScenarios = Path(__file__).parent / "Fonctionnalites" / "RechercherUnMagasin.feature"
scenarios(str(cheminScenarios))

# =============================
# SCÉNARIO 1 : Recherche par identifiant
# =============================
@given(parsers.parse('un magasin existant avec l\'identifiant {id_magasin:d}'), target_fixture="magasin")
def trouver_magasin_par_id(id_magasin, magasin_dao):
    magasin = next(m for m in magasins if m.id == id_magasin)
    magasin_dao.ajouter_magasin(magasin)
    return magasin

@when(parsers.parse('je recherche le magasin avec l\'identifiant {id_magasin:d}'), target_fixture="reponse")
def rechercher_magasin_par_id(id_magasin):
    return client.get(f"/magasins/{id_magasin}")

@then("le code de retour est 200")
def verifier_code_200(reponse):
    assert reponse.status_code == 200

@then("la réponse contient les informations du magasin (id, nom, adresse, téléphone, statut)")
def verifier_infos_magasin(reponse, magasin):
    data = reponse.json()
    validerInformationsMagasin(magasin, data)

# =============================
# SCÉNARIO 2 : Recherche par nom
# =============================
@given(parsers.parse('un magasin existant portant le nom "{nom}"'), target_fixture="magasin")
def trouver_magasin_par_nom(nom, magasin_dao):
    magasin = next((m for m in magasins if m.nom.lower() == nom.lower()), None)
    if magasin:
        magasin_dao.ajouter_magasin(magasin)
    return magasin

@when(parsers.parse('je recherche le magasin par le nom "{nom}"'), target_fixture="reponse")
def rechercher_magasin_par_nom(nom):
    return client.get(f"/magasins?nom={nom}")

@then("la réponse contient les informations du magasin (id, nom, adresse, téléphone, statut)")
def verifier_magasin_par_nom(reponse, magasin):
    data = reponse.json()
    assert data is not None, "Le magasin doit exister"
    validerInformationsMagasin(magasin, data)

# =============================
# SCÉNARIO 3 : Recherche par adresse
# =============================
@given(parsers.parse('des magasins contenant "{texte}" dans leur adresse'), target_fixture="magasins_adresse")
def trouver_magasins_par_adresse(texte):
    return [m for m in magasins if texte.lower() in m.adresse.lower()]

@when(parsers.parse('je recherche un magasin contenant "{texte}" dans son adresse'), target_fixture="reponse")
def rechercher_magasin_par_adresse(texte):
    return client.get(f"/magasins?adresse={texte}")

@then("la réponse contient la liste des magasins correspondants avec leurs informations (id, nom, adresse, téléphone, statut)")
def verifier_liste_magasins_par_adresse(reponse, magasins_adresse):
    data = reponse.json()
    assert len(data) == len(magasins_adresse)
    for idx, magasin in enumerate(magasins_adresse):
        validerInformationsMagasin(magasin, data[idx])

# =============================
# SCÉNARIO 4 : Critère inexistant
# =============================
@given(parsers.parse('aucun magasin ne correspond au critère "{critere}"'))
def verifier_critere_inexistant(critere):
    assert all(
        critere.lower() not in m.nom.lower() and critere.lower() not in m.adresse.lower()
        for m in magasins
    )

@when(parsers.parse('je recherche un magasin avec le critère inexistant "{critere}"'), target_fixture="reponse")
def rechercher_magasin_critere_inexistant(critere):
    return client.get(f"/magasins?nom={critere}")

@then("le résultat est une liste vide")
def verifier_liste_vide(reponse):
    data = reponse.json()
    assert data == [], "La liste doit être vide"

@then('le message indique "Aucun magasin ne correspond à la recherche"')
def verifier_message_aucun_magasin(reponse):
    data = reponse.json()
    assert data.get("message") == "Aucun magasin ne correspond à la recherche"
