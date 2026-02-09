from pathlib import Path
from pytest_bdd import scenarios, when, parsers
from tests.BoutEnBout.Etapes.ÉtapesCommunesFilms import *
from tests.BoutEnBout.Etapes.EtapesCommunesCollections import *


cheminScenarios = Path(__file__).parent / "Fonctionnalites" / "RechercherFilmParTitre.feature"
scenarios(str(cheminScenarios))


@when(parsers.parse('je recherche les films avec le titre "{titre}"'), target_fixture="réponse")
def rechercher_films_par_titre(client, titre):
    return client.get("/films", params={"titre": titre})
