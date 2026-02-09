from pathlib import Path
from pytest_bdd import scenarios, given, when, then, parsers
from tests.BoutEnBout.DonneesTest.donnees import magasins
from tests.BoutEnBout.DonneesTest.donnees import films
# -------------------------------------------------------------------
# Charger le feature
# -------------------------------------------------------------------
cheminScenarios = Path(__file__).parent / "Fonctionnalites" / "GererInventaire.feature"
scenarios(str(cheminScenarios))

# =============================
# Steps
# =============================

@given("un employé ou manager", target_fixture="user_role")
def employe_ou_manager():
    return {"role": "manager"}

@given("un utilisateur qui n'est pas employé ou manager", target_fixture="user_role")
def utilisateur_non_autorise():
    return {"role": "client"}

@when("il ajoute un film à l'inventaire du magasin avec une quantité valide", target_fixture="reponse")
def ajouter_film_inventaire(client, magasin_dao, user_role):
    film = films[0]
    magasin = magasins[0]
    payload = {
        "film_id": film.id,
        "magasin_id": magasin.id,
        "quantite": 5,
        "disponible": True
    }
    headers = {"Role": user_role["role"]}
    return client.post("/inventaire/ajouter", json=payload, headers=headers)

@when("il modifie la quantité ou la disponibilité d'un film dans l'inventaire", target_fixture="reponse")
def modifier_film_inventaire(client, user_role):
    film = films[0]
    magasin = magasins[0]
    payload = {"quantite": 10, "disponible": False}
    headers = {"Role": user_role["role"]}
    return client.put(f"/inventaire/{magasin.id}/{film.id}", json=payload, headers=headers)

@when("il tente d'ajouter un film avec des informations invalides", target_fixture="reponse")
def ajouter_film_invalide(client, user_role):
    payload = {"film_id": 9999, "magasin_id": 9999, "quantite": -5, "disponible": True}
    headers = {"Role": user_role["role"]}
    return client.post("/inventaire/ajouter", json=payload, headers=headers)

@when("il tente de gérer l'inventaire", target_fixture="reponse")
def utilisateur_non_autorise_gestion(client, user_role):
    payload = {"film_id": 1, "magasin_id": 1, "quantite": 5, "disponible": True}
    headers = {"Role": user_role["role"]}
    return client.post("/inventaire/ajouter", json=payload, headers=headers)

@then("le film est enregistré avec la bonne disponibilité")
def verifier_film_enregistre(magasin_dao):
    inventaire = magasin_dao.lister_inventaire()
    assert len(inventaire) == 1
    assert inventaire[0]["quantite"] == 5
    assert inventaire[0]["disponible"] is True

@then("les changements sont enregistrés et visibles dans l'inventaire")
def verifier_modification_inventaire(magasin_dao):
    inventaire = magasin_dao.lister_inventaire()
    assert inventaire[0]["quantite"] == 10
    assert inventaire[0]["disponible"] is False

@then("le système retourne 400 Bad Request")
def verifier_400(reponse):
    assert reponse.status_code == 400

@then("le système retourne 403 Forbidden")
def verifier_403(reponse):
    assert reponse.status_code == 403
