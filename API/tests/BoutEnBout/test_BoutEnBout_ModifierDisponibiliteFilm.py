from pathlib import Path
from pytest_bdd import scenarios, when
from tests.BoutEnBout.Etapes.ÉtapesCommunesFilms import *
from tests.BoutEnBout.Etapes.EtapesCommunesCollections import *


cheminScenarios = Path(__file__).parent / "Fonctionnalites" / "ModifierDisponibiliteFilm.feature"
scenarios(str(cheminScenarios))


def _creer_film_pour_disponibilite(client) -> int:
    headers = {"X-User-Role": "gestionnaire"}
    payload = {
        "id_magasin": 1,
        "titre": "Film pour test de disponibilité",
        "genre": "Action",
        "resume": "Créé uniquement pour le scénario de dispo.",
        "nbr_exemplaire_disponible": 5,
    }
    resp = client.post("/films", json=payload, headers=headers)
    assert resp.status_code == 201
    data = resp.json()
    return data["id_media"]


@when(
    "je modifie la disponibilité du film 1 avec une valeur valide",
    target_fixture="réponse",
)
def modifier_disponibilite_valide(client):
    film_id = _creer_film_pour_disponibilite(client)

    payload = {
        "nbr_exemplaire_disponible": 7,
    }
    headers = {"X-User-Role": "commis"}

    return client.patch(f"/films/{film_id}/disponibilite", json=payload, headers=headers)


@when(
    "je modifie la disponibilité du film 1 avec une valeur invalide",
    target_fixture="réponse",
)
def modifier_disponibilite_invalide(client):
    film_id = _creer_film_pour_disponibilite(client)

    payload = {
        "nbr_exemplaire_disponible": -10,
    }
    headers = {"X-User-Role": "commis"}

    return client.patch(f"/films/{film_id}/disponibilite", json=payload, headers=headers)


@when(
    "je tente de modifier la disponibilité du film 1",
    target_fixture="réponse",
)
def modifier_disponibilite_sans_droit(client):
    film_id = _creer_film_pour_disponibilite(client)

    payload = {
        "nbr_exemplaire_disponible": 3,
    }
    return client.patch(f"/films/{film_id}/disponibilite", json=payload)
