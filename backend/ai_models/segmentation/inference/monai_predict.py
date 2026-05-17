import torch
import numpy as np
import cv2

from monai.networks.nets import UNet

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model = UNet(
    spatial_dims=2,
    in_channels=3,
    out_channels=1,
    channels=(16, 32, 64, 128, 256),
    strides=(2, 2, 2, 2),
    num_res_units=2,
).to(DEVICE)

model.eval()

def preprocess_image(image_path):

    image = cv2.imread(image_path)

    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    image = cv2.resize(
        image,
        (256, 256)
    )

    image = image / 255.0

    image = np.transpose(
        image,
        (2, 0, 1)
    )

    image_tensor = torch.tensor(
        image,
        dtype=torch.float32
    ).unsqueeze(0)

    return image_tensor.to(DEVICE)

def predict_biomedical_image(image_path):

    image_tensor = preprocess_image(
        image_path
    )

    with torch.no_grad():

        prediction = model(image_tensor)

        prediction = torch.sigmoid(
            prediction
        )

    prediction = prediction.squeeze().cpu().numpy()

    prediction_mask = (
        prediction > 0.5
    ).astype(np.uint8)

    return {
        "mask": prediction_mask,
        "shape": prediction_mask.shape,
        "confidence": float(
            prediction.mean()
        )
    }