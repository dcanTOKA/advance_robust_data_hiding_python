import numpy as np
from PIL import Image
from random import seed
from random import randint
from tqdm import tqdm

seed(1)


def rgb_to_gray_scale_image(rgb):
    _, _, D = rgb.shape
    assert D == 3, "Input feature dimension is not aligned!"
    return rgb.convert('L')


def rgb_seperate(channel):
    return Image.Image.split(channel)


def to_24_bit_stream(image):
    N, D = image.size
    r, g, b = rgb_seperate(image)

    unpack_r = np.unpackbits(r, axis=1).reshape(N * D, 8)
    unpack_g = np.unpackbits(g, axis=1).reshape(N * D, 8)
    unpack_b = np.unpackbits(b, axis=1).reshape(N * D, 8)

    return np.concatenate((unpack_r, unpack_g, unpack_b), axis=1)


def randi(n):
    return randint(0, n-1)


def bit_stream_of_24_to_image(bit_stream, N, D):
    r = bit_stream[:, 0:8]
    g = bit_stream[:, 8:16]
    b = bit_stream[:, 16:24]

    r_constracted = bin_to_dec(r)
    g_constracted = bin_to_dec(g)
    b_constracted = bin_to_dec(b)

    r_reshaped = r_constracted.reshape((N, D))
    g_reshaped = g_constracted.reshape((N, D))
    b_reshaped = b_constracted.reshape((N, D))

    return image_from_array(r_reshaped, g_reshaped, b_reshaped)


def bin_to_dec(bin_list):
    dec_list = np.zeros(bin_list.shape[0])
    for ele in tqdm(range(len(bin_list)), desc="BIN TO DEC : "):
        dec_list[ele] = bin_list[ele].dot(2 ** np.arange(bin_list[ele].size)[::-1])

    return dec_list


def image_from_array(R, G, B):
    r = Image.fromarray(np.uint8(R))
    g = Image.fromarray(np.uint8(G))
    b = Image.fromarray(np.uint8(B))

    return Image.merge("RGB", (r, g, b))
