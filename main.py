from fastapi import FastAPI
from app.routes import profiles

app = FastAPI()

# Router registrieren
app.include_router(profiles.router)

@app.get("/")
def root():
    return {"message": "Welcome to the modular FastAPI application!"}
