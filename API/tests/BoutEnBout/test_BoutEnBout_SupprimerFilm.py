from pathlib import Path
from pytest_bdd import scenarios, when
from tests.BoutEnBout.Etapes.ÉtapesCommunesFilms import *
from tests.BoutEnBout.Etapes.EtapesCommunesCollections import *


cheminScenarios = Path(__file__).parent / "Fonctionnalites" / "SupprimerFilm.feature"
scenarios(str(cheminScenarios))


@when(
    "je supprime le film 1",
    target_fixture="réponse",
)
def supprimer_film_1(client):
    headers_gestionnaire = {"X-User-Role": "gestionnaire"}

    payload = {
        "id_magasin": 1,
        "titre": "Film temporaire à supprimer",
        "genre": "Action",
        "resume": "Film créé uniquement pour le scénario de suppression.",
        "nbr_exemplaire_disponible": 1,
    }
    created = client.post("/films", json=payload, headers=headers_gestionnaire)
    assert created.status_code == 201
    data = created.json()
    film_id = data["id_media"]

    return client.delete(f"/films/{film_id}", headers=headers_gestionnaire)


@when(
    "je supprime le film 999",
    target_fixture="réponse",
)
def supprimer_film_inexistant(client):
    headers = {"X-User-Role": "gestionnaire"}
    return client.delete("/films/999", headers=headers)


@when(
    "je tente de supprimer le film 1",
    target_fixture="réponse",
)
def supprimer_film_sans_manager(client):
    headers = {"X-User-Role": "commis"}
    return client.delete("/films/1", headers=headers)
