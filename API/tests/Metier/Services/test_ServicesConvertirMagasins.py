from pytest_bdd import scenarios, given, when, then, parsers
from pathlib import Path
from app.Metier.Services.MagasinsService import MagasinsService
from app.AccesAuxDonnees.DAO.MagasinsDAO import MagasinsDAO
from tests.Metier.Services.DonneesTest.donneesMagasins import magasins_test
from tests.BoutEnBout.DonneesTest.donneesMagasins import magasins

cheminScenarios = Path(__file__).parent / "Fonctionnalites" / "ConvertirMagasins.feature"
scenarios(str(cheminScenarios))


@given("un Magasin contenant 5 films", target_fixture="magasin")
def magasin_avec_films():
    return magasins_test[0]


@given("un magasin sans film", target_fixture="magasin")
def magasin_sans_film():
    magasin = magasins_test[0].model_copy(deep=True)
    magasin.films = []
    return magasin


@when("je le convertis en réponse", target_fixture="réponse")
def convertir(magasin, magasin_dao):
    return MagasinsService(magasin_dao).convertir_magasin_en_réponse(magasin)


@then(parsers.parse("le nombre de films disponibles doit être {nb_films:d}"))
def vérifier_nb_films(nb_films, réponse):
    assert réponse.nb_films_disponibles == nb_films


@then("les autres champs doivent être identiques")
def vérifier_champs(réponse):
    attendu = magasins[0]
    dict_réponse = réponse.model_dump(exclude={"nb_films_disponibles"})
    dict_attendu = attendu.model_dump(exclude={"nb_films_disponibles"})

    assert dict_réponse == dict_attendu

