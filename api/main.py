from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.predict import router as predict_router
from api.routers.registry import router as registry_router


# --- Inicialización de la aplicación FastAPI ---
app = FastAPI(
    title="Steam Sales Prediction API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(predict_router)
app.include_router(registry_router)


@app.get("/health", status_code=HTTPStatus.OK, description="Comprueba el estado de salud del servicio", tags=["Health"])
def health_check() -> dict:
    """Endpoint de salud del servicio."""
    return {"status": HTTPStatus.OK.value, "message": HTTPStatus.OK.phrase}
