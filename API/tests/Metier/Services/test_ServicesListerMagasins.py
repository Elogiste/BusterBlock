from pathlib import Path
from pytest_bdd import scenarios, given, when, then
from app.Metier.Services.MagasinsService import MagasinsService
from tests.Metier.Services.DonneesTest.donneesMagasins import magasins_test
from tests.BoutEnBout.DonneesTest.donneesMagasins import magasins

class FauxMagasinsDAO:
    def __init__(self, stations=None):
        self._stations = stations or []

    def obtenir_tous_les_magasins(self):
        return self._stations
    
chemin = Path(__file__).parent / "Fonctionnalites" / "ListerMagasins.feature"
scenarios(str(chemin))

@given("un ensemble de magasins", target_fixture="service_test")
def définir_magasins():
    faux_dao = FauxMagasinsDAO(magasins_test)
    return MagasinsService(faux_dao)

@given("aucun magasin", target_fixture="service_test")
def définir_aucun_magasin():
    faux_dao = FauxMagasinsDAO([])
    return MagasinsService(faux_dao)

@when("je liste les magasins", target_fixture="résultats")
def lister_magasin(service_test):
    return service_test.lister_magasins()

@then("la liste retournée contient tous les magasins")
def vérifier_taille(résultats):
    assert len(résultats) == len(magasins_test)

@then("chaque magasin doit être converti en réponse valide")
def vérifier_conversion(résultats):
    for magasin, réponse in zip(magasins, résultats):
        assert réponse == magasin

@then("la liste retournée doit être vide")
def vérifier_vide(résultats):
    assert résultats == []
