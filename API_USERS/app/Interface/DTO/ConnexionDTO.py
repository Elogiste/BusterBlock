from pydantic import BaseModel


class ConnexionDTO(BaseModel):
    courriel: str
    mot_de_passe: str
