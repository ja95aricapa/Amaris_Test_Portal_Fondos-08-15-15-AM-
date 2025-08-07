import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import funds_router
from models.transaction import create_table_if_not_exists

app = FastAPI(title="Gestor de Fondos API")

# Configuración de CORS para permitir peticiones desde React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # Al iniciar, crea la tabla de DynamoDB si no existe
    create_table_if_not_exists()


app.include_router(funds_router.router)


@app.get("/")
def read_root():
    return {"message": "API del Gestor de Fondos funcionando."}


# --- Entrypoint para ejecución local ---
if __name__ == "__main__":
    # Esta sección solo se ejecuta cuando corres el script directamente (ej: python main.py)
    # No se ejecuta cuando Uvicorn es iniciado por Docker.
    print("--- Iniciando servidor de desarrollo local ---")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
