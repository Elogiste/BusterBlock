from pathlib import Path
from fastapi.testclient import TestClient
from pytest_bdd import scenarios, when, parsers

from API.tests.BoutEnBout.Etapes.ÉtapesCommunesFilms import *
from tests.BoutEnBout.Etapes.EtapesCommunesCollections import *

from app.main import app

client = TestClient(app)

cheminScenarios = Path(__file__).parent / "Fonctionnalites" / "ConsulterFilms.feature"
scenarios(str(cheminScenarios))

@when(parsers.parse("je consulte les détails du film {id_film:d}"), target_fixture="réponse")
def consulterFilmParId(id_film):
    return client.get(f"/films/details/{id_film}")


@when(parsers.parse("je consulte les détails du film {id_film:d} pour le magasin {id_magasin:d}"), target_fixture="réponse")
def consulterFilmParIdEtMagasin(id_film, id_magasin):
    return client.get(f"/films/details/{id_film}?id_magasin={id_magasin}")


@when(parsers.parse('je recherche les films avec le titre "{titre}"'), target_fixture="réponse")
def rechercherFilmsParTitre(titre):
    return client.get("/films", params={"titre": titre})


@when(parsers.parse('je recherche les films du genre "{genre}"'), target_fixture="réponse")
def rechercherFilmsParGenre(genre):
    return client.get("/films", params={"genre": genre})
