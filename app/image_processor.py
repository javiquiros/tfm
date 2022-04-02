from __future__ import absolute_import, division

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet  import EfficientNetB1, preprocess_input
from tensorflow.keras.models import Model
import numpy as np


class ImageProcessor:
    def __init__(self):
        base_model = EfficientNetB1(weights='imagenet')
        self.model = Model(
            inputs=base_model.input,
            outputs=base_model.get_layer('avg_pool').output
        )
        self.image_size = self.model.input_shape[1]

    def extract_features(self, img):
        x = self.prepare_image(img)
        # (H, W, C)->(1, H, W, C), where the first elem is the number of img
        x = np.expand_dims(x, axis=0)
        # subtracting avg values for each pixel
        x = preprocess_input(x)
        # EfficientNetB1 (1, 1280) -> (1280, )
        features = self.model.predict(x)[0]
        # normalize
        return features / np.linalg.norm(features)

    def prepare_image(self, img):
        # img PIL.Image.open(path) or 
        # tensorflow.keras.preprocessing.image.load_img(path)
        # EfficientNetB1 must take a 240x240 img as input, output 1280
        img = img.resize((self.image_size, self.image_size))
        # img in color
        img = img.convert('RGB')
        # to np.array. Height x Width x Channel. dtype=float32
        return image.img_to_array(img)

    def bulk_extract_features(self, x):
        # (n, Height, Width, Channel), where the first elem is the number of img
        # subtracting avg values for each pixel
        x = preprocess_input(x)
        # EfficientNetB1 (n, 1280) -> (1280, )
        features = self.model.predict(x)
        # normalize
        for f in features:
            f = f / np.linalg.norm(f)
        return features
