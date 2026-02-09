from fastapi import FastAPI
from pathlib import Path
from dotenv import load_dotenv
import os
from app.AccesAuxDonnees.DAO.UtilisateursDAO import UtilisateursDAO
from app.Metier.Services.AuthService import AuthService
from app.Interface.Routeurs.AuthRouteur import AuthRouteur
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

bearer_scheme = HTTPBearer()

def créer_app(chemin_config: Path = None):
    if chemin_config is not None:
        load_dotenv(chemin_config)
    else:
        dotenv_par_défaut = Path(__file__).resolve().parent.parent / ".env"
        load_dotenv(dotenv_par_défaut)

    config_bd = {
        "host": os.getenv("MARIADB_HOST"),
        "user": os.getenv("MARIADB_USER"),
        "password": os.getenv("MARIADB_PASSWORD"),
        "database": os.getenv("MARIADB_DATABASE"),
        "port": int(os.getenv("MARIADB_PORT", 3306)),
    }

    dao = UtilisateursDAO(config_bd)
    service = AuthService(dao)

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_headers=["*"],
        allow_methods=["*"],
    )
   
    auth_routeur = AuthRouteur(service)
    app.include_router(auth_routeur.routeur)

    @app.get("/")
    def envoyer_saluations():
        return {"message": "Service d'authentification"}

    return app

app = créer_app()

