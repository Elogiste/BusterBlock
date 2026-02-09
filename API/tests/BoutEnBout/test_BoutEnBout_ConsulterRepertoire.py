from pathlib import Path
from pytest_bdd import scenarios, when, parsers
from tests.BoutEnBout.Etapes.ÉtapesCommunesFilms import *
from tests.BoutEnBout.Etapes.EtapesCommunesCollections import *


cheminScenarios = Path(__file__).parent / "Fonctionnalites" / "ConsulterRepertoire.feature"
scenarios(str(cheminScenarios))


@when("je consulte le répertoire des films", target_fixture="réponse")
def consulter_repertoire(client):
    return client.get("/films")


@when(parsers.parse('je recherche les films du genre "{genre}"'), target_fixture="réponse")
def rechercher_films_par_genre(client, genre):
    return client.get("/films", params={"genre": genre})


@when(parsers.parse('je recherche les films avec le titre "{titre}"'), target_fixture="réponse")
def rechercher_films_par_titre(client, titre):
    return client.get("/films", params={"titre": titre})
