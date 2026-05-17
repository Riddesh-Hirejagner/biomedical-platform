import torch

from ai_models.segmentation.unet.model import UNet

from ai_models.segmentation.preprocessing.preprocess import (
    preprocess_image
)

model = UNet()

model.eval()

def predict_segmentation(image_path):

    image_tensor = preprocess_image(
        image_path
    )

    with torch.no_grad():

        prediction = model(image_tensor)

    prediction = prediction.squeeze().numpy()

    return prediction