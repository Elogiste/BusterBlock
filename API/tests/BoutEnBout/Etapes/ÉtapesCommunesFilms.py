import pytest
from pytest_bdd import given, then, parsers
from tests.AccesAuxDonnees.DAO.DonneesTest.donnéesFilms import films_test


# ---------- GIVEN ----------

@given(parsers.parse("un film existant avec l'identifiant {id_film:d}"), target_fixture="filmAttendu")
def documenterFilmParId(id_film):
    for film in films_test:
        if film.id == id_film:
            return film
    raise AssertionError(f"Aucun film avec l'id {id_film} dans les données de test.")


@given(parsers.parse("aucun film existant avec l'identifiant {id_film:d}"))
def filmInexistant(id_film):
    pass


@given(parsers.parse("un film existant avec l'identifiant 1 disponible dans le magasin 101"))
def filmDisponibleMagasin():
    pass


@given(parsers.parse("un film existant avec l'identifiant 2 dans le magasin 101 sans exemplaire disponible"))
def filmIndisponibleMagasin():
    pass


@given("des films existent dans le système")
def desFilmsExistent():
    pass


@given("un manager authentifié")
def manager_authentifie():
    pass


@given("un employé authentifié")
def employe_authentifie():
    pass


@given("un utilisateur non manager")
def utilisateur_non_manager():
    pass


@given("un utilisateur non employé et non manager")
def utilisateur_non_employe_ni_manager():
    pass


# ---------- HELPERS ----------

def validerInformationFilm(filmRecu):
    champs_obligatoires = [
        "id_media",
        "titre",
        "genre",
        "nbr_exemplaire_disponible",
    ]
    for champ in champs_obligatoires:
        assert champ in filmRecu, f"Le champ '{champ}' est manquant dans la réponse: {filmRecu}"


# ---------- THEN ----------

@then("la réponse contient les informations détaillées du film")
def verifierInformationFilm(réponse):
    filmRecu = réponse.json()
    validerInformationFilm(filmRecu)


@then("la réponse contient au moins un film")
def verifierAuMoinsUnFilm(réponse):
    filmsRecus = réponse.json()
    assert isinstance(filmsRecus, list)
    assert len(filmsRecus) > 0


@then("la liste des films retournée est vide")
def verifierListeVide(réponse):
    filmsRecus = réponse.json()
    assert isinstance(filmsRecus, list)
    assert len(filmsRecus) == 0


@then(parsers.parse('tous les films retournés ont le genre "{genre}"'))
def verifierGenreFilms(genre, réponse):
    filmsRecus = réponse.json()
    assert isinstance(filmsRecus, list), "La réponse doit être une liste."
    assert len(filmsRecus) > 0, "Aucun film retourné alors qu'on en attendait au moins un."

    for film in filmsRecus:
        assert film["genre"].lower() == genre.lower(), (
            f"Genre inattendu pour le film '{film['titre']}': "
            f"'{film['genre']}' ≠ '{genre}'"
        )


@then("la réponse contient la liste complète du répertoire des films")
def verifierRepertoireComplet(réponse):
    filmsRecus = réponse.json()
    assert isinstance(filmsRecus, list)
    assert len(filmsRecus) >= 10
