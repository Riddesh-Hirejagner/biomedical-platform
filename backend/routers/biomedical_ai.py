from fastapi import (
    APIRouter,
    UploadFile,
    File
)

import shutil

from ai_models.segmentation.inference.monai_predict import (
    predict_biomedical_image
)

router = APIRouter()

@router.post("/analyze")

async def analyze_medical_image(
    file: UploadFile = File(...)
):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    result = predict_biomedical_image(
        file_path
    )

    confidence = round(
        result["confidence"] * 100,
        2
    )

    if confidence > 70:
        prognosis = "High abnormality probability"
        recommendation = "Immediate specialist consultation recommended"

    elif confidence > 40:
        prognosis = "Moderate abnormality detected"
        recommendation = "Further MRI/CT evaluation suggested"

    else:
        prognosis = "Low abnormality probability"
        recommendation = "Routine monitoring recommended"

    return {
        "message": "Biomedical analysis completed",
        "segmentation_shape": str(result["shape"]),
        "confidence_score": f"{confidence}%",
        "prognosis": prognosis,
        "future_recommendation": recommendation
    }