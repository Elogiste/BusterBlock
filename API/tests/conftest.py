import os
import pytest
from pathlib import Path
from dotenv import load_dotenv
from app.AccesAuxDonnees.DAO.MagasinsDAO import MagasinsDAO
from app.AccesAuxDonnees.DAO.FilmsDAO import FilmsDAO

@pytest.fixture(scope="session")
def configurer_bd_test():
    chemin_dotenv = Path(__file__).resolve().parent.parent / ".env.test"
    load_dotenv(chemin_dotenv)
    return {
        "host": os.getenv("MARIADB_HOST"),
        "user": os.getenv("MARIADB_USER"),
        "password": os.getenv("MARIADB_PASSWORD"),
        "database": os.getenv("MARIADB_DATABASE"),
        "port": int(os.getenv("MARIADB_PORT", 3306))
    }

@pytest.fixture(scope="session")
def magasin_dao(configurer_bd_test):
    magasindao = MagasinsDAO(configurer_bd_test)
    magasindao.vider_tables(["magasins", "films"])
    yield magasindao
    magasindao.vider_tables(["magasins", "films"])
    
@pytest.fixture(scope="session")
def films_dao(configurer_bd_test):
    dao = FilmsDAO(configurer_bd_test)
    dao.vider_tables(["films"])
    yield dao
    dao.vider_tables(["films"])
    

from fastapi.testclient import TestClient
from app.main import créer_app  # ou 'from app.main import app' si app est déjà instanciée

@pytest.fixture
def client():
    """
    Fixture FastAPI TestClient pour les tests BDD
    """
    app = créer_app()  # ou simplement 'app' si app est déjà créé
    return TestClient(app)