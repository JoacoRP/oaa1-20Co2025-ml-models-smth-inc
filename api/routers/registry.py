from http import HTTPStatus
from typing import List

from fastapi import APIRouter, HTTPException

from api.services.registry_service import get_predictions
from api.models.schemas import RegistryEntry


router = APIRouter(prefix="/registry", tags=["Registry"])

@router.get("/", response_model=List[RegistryEntry], status_code=HTTPStatus.OK, description="Devuelve todas las entradas del registro de predicciones")
def list_registry(skip: int = 0, limit: int = 100) -> List[RegistryEntry]:
    """Lista el registro de predicciones."""
    try:
        entries = get_predictions(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Error al recuperar el registro: {e}"
        )
    return entries
