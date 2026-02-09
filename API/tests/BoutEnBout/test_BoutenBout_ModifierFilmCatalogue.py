from pathlib import Path
from pytest_bdd import scenarios, when
from tests.BoutEnBout.Etapes.ÉtapesCommunesFilms import *
from tests.BoutEnBout.Etapes.EtapesCommunesCollections import *


cheminScenarios = Path(__file__).parent / "Fonctionnalites" / "ModifierFilmCatalogue.feature"
scenarios(str(cheminScenarios))


def _creer_film_catalogue(client):
    """
    Crée un film « jetable » qui servira de cible aux scénarios
    de modification du catalogue. Retourne (id_media, id_magasin).
    """
    headers = {"X-User-Role": "gestionnaire"}
    payload = {
        "id_magasin": 1,
        "titre": "Film à modifier",
        "genre": "Action",
        "resume": "Film créé pour le scénario de modification.",
        "nbr_exemplaire_disponible": 5,
    }
    resp = client.post("/films", json=payload, headers=headers)
    assert resp.status_code == 201
    data = resp.json()
    return data["id_media"], 1


@when(
    "je modifie le film 1 avec des données valides",
    target_fixture="réponse",
)
def modifier_film_1_valide(client):
    film_id, id_magasin = _creer_film_catalogue(client)

    payload = {
        "id_media": film_id,
        "id_magasin": id_magasin,
        "titre": "La guerre des étoiles - Version restaurée",
        "genre": "Science-Fiction",
        "resume": "La bible mais dans l'espace (version restaurée)",
        "nbr_exemplaire_disponible": 10,
    }
    headers = {"X-User-Role": "gestionnaire"}

    return client.put(f"/films/{film_id}", json=payload, headers=headers)


@when(
    "je modifie le film 1 avec des données invalides",
    target_fixture="réponse",
)
def modifier_film_1_invalide(client):
    film_id, id_magasin = _creer_film_catalogue(client)

    payload = {
        "id_media": film_id,
        "id_magasin": id_magasin,
        "titre": "",
        "genre": "Science-Fiction",
        "resume": "Résumé invalide",
        "nbr_exemplaire_disponible": -5,
    }
    headers = {"X-User-Role": "gestionnaire"}

    return client.put(f"/films/{film_id}", json=payload, headers=headers)


@when(
    "je modifie le film 999 avec des données valides",
    target_fixture="réponse",
)
def modifier_film_inexistant_valide(client):
    payload = {
        "id_media": 999,
        "id_magasin": 1,
        "titre": "Film inexistant",
        "genre": "Action",
        "resume": "Résumé",
        "nbr_exemplaire_disponible": 1,
    }
    headers = {"X-User-Role": "gestionnaire"}
    return client.put("/films/999", json=payload, headers=headers)


@when(
    "je tente de modifier le film 1",
    target_fixture="réponse",
)
def modifier_film_sans_manager(client):
    film_id, id_magasin = _creer_film_catalogue(client)

    payload = {
        "id_media": film_id,
        "id_magasin": id_magasin,
        "titre": "Titre modifié par utilisateur non manager",
        "genre": "Science-Fiction",
        "resume": "Résumé",
        "nbr_exemplaire_disponible": 3,
    }
    headers = {"X-User-Role": "commis"}

    return client.put(f"/films/{film_id}", json=payload, headers=headers)
