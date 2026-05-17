from fastapi import (
    APIRouter,
    UploadFile,
    File
)

import shutil

router = APIRouter()

@router.post("/image")
async def upload_image(
    file: UploadFile = File(...)
):

    file_location = f"uploads/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "message": "Image uploaded successfully",
        "filename": file.filename
    }