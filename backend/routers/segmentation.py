from fastapi import (
    APIRouter,
    UploadFile,
    File
)

import shutil

from ai_models.segmentation.inference.predict import (
    predict_segmentation
)

router = APIRouter()

@router.post("/segment")

async def segment_image(
    file: UploadFile = File(...)
):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    prediction = predict_segmentation(
        file_path
    )

    return {
        "message": "Segmentation completed",
        "prediction_shape": str(
            prediction.shape
        )
    }