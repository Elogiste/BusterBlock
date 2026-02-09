import pytest
from app.dao.FilmsDao import FilmDAO
from app.Metier.Services.FilmsService import FilmService


@pytest.fixture
def service():
    dao = FilmDAO()
    return FilmService(dao=dao)


def test_chercher_films_sans_filtre_retourne_tous_les_films(service):
    films = service.chercher_films()
    assert len(films) >= 10

    titres = {film.titre for film in films}
    for titre_attendu in {
        "Le Dernier Combat",
        "Amour de Neige",
        "Réalité Virtuelle",
        "Cuisine en Folie",
    }:
        assert titre_attendu in titres


def test_chercher_films_par_titre(service):
    films = service.chercher_films(titre="Combat")
    assert len(films) >= 1
    assert any("dernier combat" in f.titre.lower() for f in films)


def test_chercher_films_par_genre(service):
    films = service.chercher_films(genre="Science-fiction")
    assert len(films) >= 2
    assert all(f.genre.lower() == "science-fiction" for f in films)


def test_obtenir_details_film_existant_sans_magasin(service):
    film = service.obtenir_details_film(id_film=1)
    assert film is not None
    assert film.id_media == 1
    assert film.titre == "Le Dernier Combat"
    assert film.est_disponible_dans_ce_magasin is None


def test_obtenir_details_film_existant_avec_magasin_disponible(service):
    film = service.obtenir_details_film(id_film=1, id_magasin=1)
    assert film is not None
    assert film.id_media == 1
    assert film.est_disponible_dans_ce_magasin is True


def test_obtenir_details_film_existant_avec_magasin_indisponible(service):
    film = service.obtenir_details_film(id_film=2, id_magasin=1)
    assert film is not None
    assert film.id_media == 2
    assert film.est_disponible_dans_ce_magasin is False


def test_obtenir_details_film_inexistant_retourne_none(service):
    film = service.obtenir_details_film(id_film=9999)
    assert film is None
