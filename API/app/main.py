from fastapi import FastAPI, Depends
from pathlib import Path
import os
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware

from app.Interface.Securite.auth0 import exiger_jeton
from app.Interface.Routeurs.MagasinsRouteur import MagasinsRouteur
from app.Interface.Routeurs.FilmsRouteur import router as films_router

from app.AccesAuxDonnees.DAO.MagasinsDAO import MagasinsDAO
from app.Metier.Services.MagasinsService import MagasinsService


def créer_app(chemin_config: Path = None):
    if chemin_config:
        load_dotenv(chemin_config)
    else:
        dotenv_path = Path(__file__).resolve().parent.parent / ".env"
        load_dotenv(dotenv_path)

    config_bd = {
        "host": os.getenv("MARIADB_HOST"),
        "user": os.getenv("MARIADB_USER"),
        "password": os.getenv("MARIADB_PASSWORD"),
        "database": os.getenv("MARIADB_DATABASE"),
        "port": int(os.getenv("MARIADB_PORT", 3306)),
    }

    magasin_dao = MagasinsDAO(config_bd)
    magasin_service = MagasinsService(magasin_dao)

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ROUTERS
    app.include_router(MagasinsRouteur(magasin_service).routeur)
    app.include_router(films_router)

    @app.get("/")
    def racine():
        return {"message": "Bonjour, API publique!"}

    @app.get("/role-test")
    def role_test(user: dict = Depends(exiger_jeton)):
        return {"message": f"Bonjour {user.get('nom')}", "roles": user.get("roles")}

    return app


app = créer_app()
