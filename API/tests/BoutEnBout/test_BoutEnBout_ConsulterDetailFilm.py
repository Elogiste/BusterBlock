from pathlib import Path
from pytest_bdd import scenarios, when, parsers
from tests.BoutEnBout.Etapes.ÉtapesCommunesFilms import *
from tests.BoutEnBout.Etapes.EtapesCommunesCollections import *


cheminScenarios = Path(__file__).parent / "Fonctionnalites" / "ConsulterDetailFilm.feature"
scenarios(str(cheminScenarios))


@when(parsers.parse("je consulte les détails du film {id_film:d}"), target_fixture="réponse")
def consulter_film_par_id(client, id_film: int):
    return client.get(f"/films/details/{id_film}")


@when(
    parsers.parse("je consulte les détails du film {id_film:d} pour le magasin {id_magasin:d}"),
    target_fixture="réponse",
)
def consulter_film_par_id_et_magasin(client, id_film: int, id_magasin: int):
    return client.get(f"/films/details/{id_film}?id_magasin={id_magasin}")
