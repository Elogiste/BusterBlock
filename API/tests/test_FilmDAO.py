import pytest
from app.dao.FilmsDao import FilmDAO


@pytest.fixture
def dao():
    return FilmDAO()


def test_lister_films_sans_filtre_retourne_tous_les_films(dao):
    films = dao.lister_films()
    assert len(films) >= 10

    titres = {film.titre for film in films}
    for titre_attendu in {
        "Le Dernier Combat",
        "Amour de Neige",
        "Réalité Virtuelle",
        "Cuisine en Folie",
    }:
        assert titre_attendu in titres


def test_lister_films_filtre_par_titre_partiel(dao):
    films = dao.lister_films(titre="Combat")
    assert len(films) >= 1
    assert any("dernier combat" in f.titre.lower() for f in films)


def test_lister_films_filtre_par_genre(dao):
    films = dao.lister_films(genre="Science-fiction")
    assert len(films) >= 2
    assert all(f.genre.lower() == "science-fiction" for f in films)


def test_lister_films_filtre_par_disponible_true(dao):
    films = dao.lister_films(disponible=True)
    assert len(films) >= 1
    assert all(f.nbr_exemplaire_disponible > 0 for f in films)


def test_lister_films_filtre_par_disponible_false(dao):
    films = dao.lister_films(disponible=False)
    assert len(films) >= 1
    assert all(f.nbr_exemplaire_disponible == 0 for f in films)


def test_obtenir_film_par_id_existant(dao):
    film = dao.obtenir_film_par_id(1)
    assert film is not None
    assert film.id_media == 1
    assert film.titre == "Le Dernier Combat"


def test_obtenir_film_par_id_inexistant(dao):
    film = dao.obtenir_film_par_id(9999)
    assert film is None


def test_verifier_disponibilite_film_disponible_dans_magasin(dao):
    est_dispo = dao.verifier_disponibilite(id_film=1, id_magasin=1)
    assert est_dispo is True


def test_verifier_disponibilite_film_indisponible_dans_magasin(dao):
    est_dispo = dao.verifier_disponibilite(id_film=2, id_magasin=1)
    assert est_dispo is False


def test_verifier_disponibilite_aucune_entree_inventaire(dao):
    est_dispo = dao.verifier_disponibilite(id_film=1, id_magasin=999)
    assert est_dispo is False
