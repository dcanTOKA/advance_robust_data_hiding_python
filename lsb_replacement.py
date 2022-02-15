from utils import *
import numpy as np


class LsbReplacement:
    def __init__(self, shares, envelopes, n):
        self.N_env, self.D_env, _ = np.asarray(envelopes[0]).shape
        self.N_shr, self.D_shr, _ = shares[0].shape
        self.shares = shares
        self.envelopes = envelopes
        self.enveloped_shares = []
        self.retrieved_shares = []
        self.n = n
        assert n == len(envelopes), "Envelope size and share size must be same !"

    def lsb_replace(self):
        for index in range(self.n):
            envelope_bit_stream = to_24_bit_stream(self.envelopes[index])
            share_bit_stream_flatten = to_24_bit_stream(
                Image.fromarray(self.shares[index].astype('uint8'), 'RGB')).flatten()

            row_size = envelope_bit_stream.shape[0]
            column_size = envelope_bit_stream.shape[1]

            for row in tqdm(range(row_size), desc=f"LSB Replacement for share {index + 1}"):
                temp_envelope_row_bit_stream = envelope_bit_stream[row, :]
                temp_envelope_row_bit_stream[column_size - 1] = share_bit_stream_flatten[(row * 2)]
                temp_envelope_row_bit_stream[column_size - 8 - 1] = share_bit_stream_flatten[(row * 2) + 1]
                envelope_bit_stream[row, :] = temp_envelope_row_bit_stream
                if (row * 2) == (share_bit_stream_flatten.shape[0] - 1 - 2):
                    break

            self.enveloped_shares.append(bit_stream_of_24_to_image(envelope_bit_stream, self.N_env, self.D_env))
            bit_stream_of_24_to_image(envelope_bit_stream, self.N_env, self.D_env).show()

    def lsb_retrieve(self):
        for index in range(self.n):
            enveloped_shares_bit_stream = to_24_bit_stream(self.enveloped_shares[index])

            row_size = enveloped_shares_bit_stream.shape[0]
            column_size = enveloped_shares_bit_stream.shape[1]

            flatten_share = np.zeros(self.N_shr * self.D_shr * column_size).flatten()

            for row in range(row_size):
                flatten_share[(row * 2)] = enveloped_shares_bit_stream[row, column_size - 1]
                flatten_share[(row * 2) + 1] = enveloped_shares_bit_stream[row, column_size - 8 - 1]
                if row == row_size - 2:
                    break

            retrieved_share = bit_stream_of_24_to_image(flatten_share.reshape((self.N_shr * self.D_shr, column_size)),
                                                        self.N_shr, self.D_shr)
            retrieved_share.show()
            self.retrieved_shares.append(retrieved_share)
        return self.retrieved_shares
