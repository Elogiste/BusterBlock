from pathlib import Path
from pytest_bdd import scenarios, when
from tests.BoutEnBout.Etapes.ÉtapesCommunesFilms import *
from tests.BoutEnBout.Etapes.EtapesCommunesCollections import *


cheminScenarios = Path(__file__).parent / "Fonctionnalites" / "AjouterFilm.feature"
scenarios(str(cheminScenarios))


@when(
    "j'ajoute un nouveau film avec des informations valides",
    target_fixture="réponse",
)
def ajouter_film_valide(client):
    payload = {
        "id_magasin": 1,
        "titre": "Nouveau film BusterBlock",
        "genre": "Action",
        "resume": "Un tout nouveau film d'action.",
        "nbr_exemplaire_disponible": 5,
    }
    headers = {"X-User-Role": "gestionnaire"}
    return client.post("/films", json=payload, headers=headers)


@when(
    "j'ajoute un nouveau film avec des informations invalides",
    target_fixture="réponse",
)
def ajouter_film_invalide(client):
    payload = {
        "id_magasin": 1,
        "titre": "",
        "genre": "",
        "resume": "Film avec données invalides.",
        "nbr_exemplaire_disponible": -1,
    }
    headers = {"X-User-Role": "gestionnaire"}
    return client.post("/films", json=payload, headers=headers)
