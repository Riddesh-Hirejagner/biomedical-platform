from fastapi import (
    APIRouter,
    UploadFile,
    File
)

import shutil

from ai_models.classification.chest_xray import (
    predict_xray
)

router = APIRouter()
@router.post("/xray/analyze")

async def analyze_xray(
    file: UploadFile = File(...)
):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    predictions = predict_xray(
        file_path
    )

    top_findings = [
        (disease, score)
        for disease, score in predictions.items()
        if score > 75
    ]

    top_findings = sorted(
        top_findings,
        key=lambda x: x[1],
        reverse=True
    )

 if len(top_findings) == 0:

        return {
            "message": "Chest X-ray analysis completed",
            "interpretation":
                "No major abnormalities detected",
            "risk_level": "Low",
            "future_recommendation":
                "Routine monitoring recommended"
        }

    return {
        "message": "Chest X-ray analysis completed",
        "risk_level": "Moderate/High",
        "top_findings": top_findings,
        "future_recommendation":
            "Further clinical evaluation recommended"
    }