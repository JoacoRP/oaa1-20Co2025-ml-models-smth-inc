from datetime import datetime, UTC

from sqlalchemy import Column, Integer, Float, DateTime, JSON

from api.database import Base


class PredictionRegistry(Base):
    """Modelo de ORM para el registro de predicciones."""
    __tablename__ = "prediction_registry"

    id = Column(Integer, primary_key=True, index=True)
    input_data = Column(JSON, nullable=False)
    prediction = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(UTC))