from app.core.simulation import simulation
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Bienvenido a la aplicación FastAPI"}

@app.post("/reportes")
def generate_simulation(hectares: float, tramps: int, insecticide_eggs: bool | None, prev_larvaes: int | None)
    data = simulation(hectares, tramps, insecticide_eggs, prev_larvaes)
    return data