import cv2
import numpy as np
import torch

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
    )

    image_tensor = image_tensor.unsqueeze(0)

    return image_tensor