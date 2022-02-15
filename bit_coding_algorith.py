import numpy as np
from PIL import Image
from utils import *


class Bitplane:
    def __init__(self, red_cover, green_cover, blue_cover, secret):
        self.bit_plane_to_code = 2
        self.first_msb_choice_of_secret = 0
        self.second_msb_choice_of_secret = 1
        self.third_msb_choice_of_secret = 2

        self.N, self.D = secret.size
        self.number_of_plane = 0

        self.red_cover_bit_plains = self.bit_plain_generator(red_cover).astype(int)
        self.green_cover_bit_plains = self.bit_plain_generator(green_cover).astype(int)
        self.blue_cover_bit_plains = self.bit_plain_generator(blue_cover).astype(int)
        self.secret_bit_planes = self.bit_plain_generator(secret).astype(int)

    def bit_plain_generator(self, image):
        N, D = image.size
        image_bit_planes = np.unpackbits(image, axis=1).reshape(N * D, 8)
        self.number_of_plane = image_bit_planes.shape[-1]

        bit_planes = np.zeros((self.number_of_plane, N, D))

        for i in range(self.number_of_plane):
            bit_planes[i, :, :] = image_bit_planes[:, i].reshape((N, D))

        return bit_planes

    def create_stego_image(self):
        new_r = self.bit_plane_coding(self.red_cover_bit_plains, self.bit_plane_to_code, self.secret_bit_planes,
                                      self.first_msb_choice_of_secret)
        new_g = self.bit_plane_coding(self.green_cover_bit_plains, self.bit_plane_to_code, self.secret_bit_planes,
                                      self.second_msb_choice_of_secret)
        new_b = self.bit_plane_coding(self.blue_cover_bit_plains, self.bit_plane_to_code, self.secret_bit_planes,
                                      self.third_msb_choice_of_secret)

        return image_from_array(new_r, new_g, new_b)

    def bit_plane_coding(self, bit_plane, cover_index, secret_plain, secret_index):
        bit_plane[cover_index, :, :] = secret_plain[secret_index, :, :]
        return self.reconstruct_image(bit_plane)

    @staticmethod
    def reconstruct_image(bit_planes):
        reconstruct = bit_planes[0, :, :]

        for a in range(7):
            reconstruct = 2 * reconstruct + bit_planes[a + 1, :, :]

        return reconstruct

    def bit_plane_decoding(self, stego):
        r, g, b = rgb_seperate(stego)
        r_bit_plane = self.bit_plain_generator(r)
        g_bit_plane = self.bit_plain_generator(g)
        b_bit_plane = self.bit_plain_generator(b)

        temp = np.zeros((self.number_of_plane, self.N, self.D))

        temp[self.first_msb_choice_of_secret, :, :] = r_bit_plane[self.bit_plane_to_code, :, :]
        temp[self.second_msb_choice_of_secret, :, :] = g_bit_plane[self.bit_plane_to_code, :, :]
        temp[self.third_msb_choice_of_secret, :, :] = b_bit_plane[self.bit_plane_to_code, :, :]

        reconstructed_secret = Image.fromarray(self.reconstruct_image(temp))
        reconstructed_secret.show()
        return reconstructed_secret

