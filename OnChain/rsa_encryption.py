from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

class RSAEncryption:
    def __init__(self):
        self.key = RSA.generate(2048)
        self.public_key = self.key.publickey().export_key()
        self.private_key = self.key.export_key()

    def encrypt(self, data):
        cipher = PKCS1_OAEP.new(RSA.import_key(self.public_key))
        encrypted_data = cipher.encrypt(data.encode())
        return base64.b64encode(encrypted_data).decode()

    def decrypt(self, encrypted_data, private_key):
        cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
        decrypted_data = cipher.decrypt(base64.b64decode(encrypted_data))
        return decrypted_data.decode()
