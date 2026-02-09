from typing import List, Dict, Any, Optional
from fastapi import Depends, HTTPException, status, Header


def obtenir_role(x_user_role: Optional[str] = Header(None)) -> Dict[str, Any]:
    role = (x_user_role or "").strip().lower()
    roles: List[str] = [role] if role else []
    return {"roles": roles}


def exiger_roles(roles_requis: List[str]):
    def dépendance(payload: Dict[str, Any] = Depends(obtenir_role)) -> Dict[str, Any]:
        roles = payload.get("roles", [])
        if not any(role in roles for role in roles_requis):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès interdit : rôle insuffisant.",
            )
        return payload

    return dépendance


manager_requis = exiger_roles(["gestionnaire", "admin"])
employe_ou_manager_requis = exiger_roles(["commis", "gestionnaire", "admin"])
