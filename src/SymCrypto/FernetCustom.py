from cryptography.fernet import Fernet

class FernetCustom:
    def __init__(self, key):
        self.f = Fernet(key)

    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    def encrypt(self, message):
        return self.f.encrypt(message.encode("utf-8"))

    def decrypt(self, message):
        bin_message = self.f.decrypt(message)
        return bin_message.decode('utf-8')
