from cryptography.fernet import Fernet
import base64
class FernetCustom:
    def __init__(self, key):
        self.f = Fernet(base64.urlsafe_b64encode(key))

    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    def encrypt(self, message):
        return self.f.encrypt(message.encode("utf-8"))

    def decrypt(self, message):
        bin_message = self.f.decrypt(message)
        return bin_message.decode('utf-8')
