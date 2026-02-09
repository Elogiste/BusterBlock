import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_consulter_details_par_id_succes():
    response = client.get("/films/details/1")
    assert response.status_code == 200
    data = response.json()

    assert data["id_media"] == 1
    assert data["titre"] == "Le Dernier Combat"
    assert data["est_disponible_dans_ce_magasin"] is None


def test_consulter_details_film_non_trouve():
    response = client.get("/films/details/9999")
    assert response.status_code == 404
    assert "Film avec ID 9999 non trouvé." in response.json()["detail"]


def test_disponibilite_magasin_succes_disponible():
    response = client.get("/films/details/1?id_magasin=1")
    assert response.status_code == 200
    data = response.json()

    assert data["id_media"] == 1
    assert data["est_disponible_dans_ce_magasin"] is True


def test_disponibilite_magasin_succes_non_disponible():
    response = client.get("/films/details/2?id_magasin=1")
    assert response.status_code == 200
    data = response.json()

    assert data["id_media"] == 2
    assert data["est_disponible_dans_ce_magasin"] is False
