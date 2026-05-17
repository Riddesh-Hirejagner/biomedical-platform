from fastapi import FastAPI
from database.database import engine
from routers.auth import router as auth_router
from routers.upload import router as upload_router
from routers.segmentation import router as segmentation_router
from routers.biomedical_ai import router as biomedical_router
app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Biomedical AI Backend Running"
    }

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)
app.include_router(
    upload_router,
    prefix="/upload",
    tags=["Upload"]
)
from database.database import Base, engine
from models.user import User

Base.metadata.create_all(bind=engine)

app.include_router(
    biomedical_router,
    prefix="/biomedical",
    tags=["Biomedical AI"]
)