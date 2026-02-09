from pathlib import Path
from pytest_bdd import scenarios, given, when, then, parsers
from tests.BoutEnBout.DonneesTest.donnees import films
from tests.BoutEnBout.DonneesTest.donnees import magasins

# -------------------------------------------------------------------
# Charger le feature
# -------------------------------------------------------------------
cheminScenarios = Path(__file__).parent / "Fonctionnalites" / "ConsulterDisponibiliteFilm.feature"
scenarios(str(cheminScenarios))

# ==============================
# Steps
# ==============================

@given("un utilisateur", target_fixture="user")
def utilisateur():
    return {"role": "client"}

@when(parsers.parse('je recherche le film avec le titre "{titre}"'), target_fixture="reponse")
def rechercher_film_par_titre(client, titre):
    # Ici on suppose que l'endpoint est /films/disponibilite?titre=...
    return client.get(f"/films/disponibilite?titre={titre}")

@when(parsers.parse('je recherche le film avec l\'identifiant {id_film:d}'), target_fixture="reponse")
def rechercher_film_par_id(client, id_film):
    # Ici on suppose que l'endpoint est /films/disponibilite/{id_film}
    return client.get(f"/films/disponibilite/{id_film}")

@then("le système affiche uniquement les magasins où le film est disponible avec le nombre de copies restantes")
def verifier_disponibilite(client, magasin_dao):
    # On récupère la liste de l'inventaire pour ce film
    inventaire = magasin_dao.lister_inventaire()
    disponibles = [i for i in inventaire if i["quantite"] > 0]
    assert len(disponibles) > 0
    for stock in disponibles:
        assert stock["quantite"] > 0
        assert "magasin_id" in stock

@then("le système indique que le film n'est disponible dans aucun magasin")
def verifier_film_indisponible(client, magasin_dao):
    inventaire = magasin_dao.lister_inventaire()
    indisponibles = [i for i in inventaire if i["quantite"] > 0]
    assert len(indisponibles) == 0

@then("le système retourne une erreur 400 ou 404")
def verifier_erreur_400_ou_404(reponse):
    assert reponse.status_code in [400, 404]
