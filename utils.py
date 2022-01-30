import numpy as np
from PIL import Image


def rgb_to_gray_scale_image(rgb):
    _, _, D = rgb.shape
    assert D == 3, "Input feature dimension is not aligned!"
    return rgb.convert('L')


def rgb_seperate(channel):
    return Image.Image.split(channel)