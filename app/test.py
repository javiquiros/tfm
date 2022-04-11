import os
import numpy
from PIL import Image

image = Image.open("app/static/images/1.png").convert('RGBA')


def image_to_vector(image: numpy.ndarray) -> numpy.ndarray:
    """
    Args:
    image: numpy array of shape (length, height, depth)

    Returns:
     v: a vector of shape (length x height x depth, 1)
    """
    data = numpy.array(image)
    flat_arr = data.ravel()
    length, height, depth = data.shape
    reshaped_image = data.reshape((length * height * depth, 1))
    return numpy.concatenate(reshaped_image)
