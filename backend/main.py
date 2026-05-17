from fastapi import FastAPI
from database.database import engine

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Biomedical AI Backend Running"
    }