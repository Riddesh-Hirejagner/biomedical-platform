import torch
import cv2
import numpy as np
import torchxrayvision as xrv

model = xrv.models.DenseNet(
    weights="densenet121-res224-all"
)

model.eval()

pathologies = model.pathologies

def preprocess_xray(image_path):

    image = cv2.imread(
        image_path,
        cv2.IMREAD_GRAYSCALE
    )

    image = cv2.resize(
        image,
        (224, 224)
    )

    image = image.astype(np.float32)

    image = image / 255.0

    image = np.expand_dims(
        image,
        axis=0
    )

    image = np.expand_dims(
        image,
        axis=0
    )

    image_tensor = torch.tensor(
        image,
        dtype=torch.float32
    )

    return image_tensor

def predict_xray(image_path):

    image_tensor = preprocess_xray(
        image_path
    )

    with torch.no_grad():

        outputs = model(image_tensor)

    outputs = outputs[0].numpy()

    predictions = {}

    for pathology, score in zip(
        pathologies,
        outputs
    ):

        predictions[pathology] = round(
            float(score) * 100,
            2
        )

    return predictions