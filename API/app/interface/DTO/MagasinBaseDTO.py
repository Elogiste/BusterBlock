from pydantic import BaseModel, field_validator
from typing import Optional

class MagasinBaseDTO(BaseModel):
    nom: Optional[str] = None
    adresse: Optional[str] = None
    telephone: Optional[str] = None
    status: Optional[bool] = None

    @field_validator("nom", check_fields=False)
    @classmethod
    def valider_nom(cls, valeur):
        if valeur is not None and not valeur.strip():
            raise ValueError("Le nom du magasin ne peut pas être vide.")
        return valeur.strip() if valeur else valeur

    @field_validator("adresse", check_fields=False)
    @classmethod
    def valider_adresse(cls, valeur):
        if valeur is not None and not valeur.strip():
            raise ValueError("L'adresse du magasin ne peut pas être vide.")
        return valeur.strip() if valeur else valeur

    @field_validator("telephone", check_fields=False)
    @classmethod
    def valider_telephone(cls, valeur):
        if valeur is not None and not valeur.strip():
            raise ValueError("Le téléphone du magasin ne peut pas être vide.")
        return valeur.strip() if valeur else valeur

    def __eq__(self, other):
        if not isinstance(other, BaseModel):
            return NotImplemented

        champs_self = set(self.__class__.model_fields.keys())
        champs_other = set(other.__class__.model_fields.keys())
        champs_communs = champs_self & champs_other

        for champ in champs_communs:
            val1 = getattr(self, champ)
            val2 = getattr(other, champ)

            if isinstance(val1, float) and isinstance(val2, float):
                from math import isclose
                if not isclose(val1, val2, rel_tol=1e-6, abs_tol=1e-6):
                    return False
            else:
                if val1 != val2:
                    return False

        return True
