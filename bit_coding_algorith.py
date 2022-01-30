import numpy as np
from PIL import Image


class Bitplane:
    def __init__(self, red_cover, green_cover, blue_cover, secret):
        self.bit_plane_to_code = 2
        self.first_msb_choice_of_secret = 0
        self.second_msb_choice_of_secret = 1
        self.third_msb_choice_of_secret = 2

        self.N, self.D = secret.size

        self.red_cover_bit_plains = self.bit_plain_generator(red_cover).astype(int)
        self.green_cover_bit_plains = self.bit_plain_generator(green_cover).astype(int)
        self.blue_cover_bit_plains = self.bit_plain_generator(blue_cover).astype(int)
        self.secret_bit_planes = self.bit_plain_generator(secret).astype(int)

    def bit_plain_generator(self, image):
        N, D = image.size
        image_bit_planes = np.unpackbits(image, axis=1).reshape(N * D, 8)
        number_of_plane = image_bit_planes.shape[-1]

        bit_planes = np.zeros((number_of_plane, N, D))

        for i in range(number_of_plane):
            bit_planes[i, :, :] = image_bit_planes[:, i].reshape((N, D))

        return bit_planes

    def create_stego_image(self):
        new_r = self.bit_plane_coding(self.red_cover_bit_plains, self.bit_plane_to_code, self.secret_bit_planes,
                                      self.first_msb_choice_of_secret)
        new_g = self.bit_plane_coding(self.green_cover_bit_plains, self.bit_plane_to_code, self.secret_bit_planes,
                                      self.second_msb_choice_of_secret)
        new_b = self.bit_plane_coding(self.blue_cover_bit_plains, self.bit_plane_to_code, self.secret_bit_planes,
                                      self.third_msb_choice_of_secret)

        r = Image.fromarray(np.uint8(new_r))
        g = Image.fromarray(np.uint8(new_g))
        b = Image.fromarray(np.uint8(new_b))

        return Image.merge("RGB", (r, g, b))

    def bit_plane_coding(self, bit_plane, cover_index, secret_plain, secret_index):
        bit_plane[cover_index, :, :] = secret_plain[secret_index, :, :]
        return self.reconstruct_image(bit_plane)

    @staticmethod
    def reconstruct_image(bit_planes):
        reconstruct = bit_planes[0, :, :]

        for a in range(7):
            reconstruct = 2 * reconstruct + bit_planes[a + 1, :, :]

        return reconstruct
