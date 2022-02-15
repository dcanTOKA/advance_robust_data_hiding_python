from bit_coding_algorith import *
from data import *
from kn_secret_sharing import *
from lsb_replacement import *


images = Images()

# Get cover image
cover = images.get_cover('lena.jpeg')

# Get secret image
secret = images.get_secret('cameraman.png')

# get envelopes images
envelopes = images.get_envelopes()

# R G and B separated channels
red_cover, green_cover, blue_cover = rgb_seperate(cover)

# create an instance and pass all cover 
bit_plane = Bitplane(red_cover, green_cover, blue_cover, secret)

# create a stego image after applying bit-coding algorithm
recombined_image = bit_plane.create_stego_image()

recombined_image.show()

k = 5
n = 6
recons = n - k + 1

kn_secret_sharing = KnSharing(recombined_image, k, n, recons)

shares = kn_secret_sharing.create_shares()

#decrypt_shares = kn_secret_sharing.decrypt_shares()

steganography = LsbReplacement(shares, envelopes, n)

steganography.lsb_replace()

taken = steganography.lsb_retrieve()

decrypt_shares = kn_secret_sharing.decrypt_shares(taken)

