import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class AEAD:
    def __init__(self, key):
        self.aead = AESGCM(key)

    """
    Generate the key and nonce for the AEAD algorithm.
    :param key_size: Size of the key, which must be 128, 192 or 256
    :return key generated and nonce
    """

    @staticmethod
    def generate_key(key_size=128):
        return AESGCM.generate_key(key_size), os.urandom(12)

    def encrypt(self, message, nonce, associated_data=None):
        return self.aead.encrypt(nonce, message.encode('utf-8'), associated_data)

    def decrypt(self, message, nonce, associated_data=None):
        bin_message = self.aead.decrypt(nonce, message, associated_data)
        return bin_message.decode('utf-8')
