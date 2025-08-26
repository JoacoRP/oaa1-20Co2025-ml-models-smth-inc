from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    """Esquema de entrada para predicción de ventas."""
    day_of_week: int = Field(..., alias="DayOfWeek", description="1=lunes, ..., 7=domingo")
    season: int = Field(..., alias="Season", description="1=verano, 2=otoño, 3=invierno, 4=primavera")
    holiday: int = Field(..., alias="Holiday", description="0=no feriado, 1=feriado")

    class Config:
        allow_population_by_alias = True


class PredictionOutput(BaseModel):
    """Esquema de salida de la predicción."""
    prediction: float = Field(..., description="Valor de ventas predicho")


class RegistryEntry(BaseModel):
    """Esquema para una entrada del registro de predicciones."""
    id: int
    input_data: Dict[str, Any]
    prediction: float
    timestamp: datetime

    class Config:
        orm_mode = True