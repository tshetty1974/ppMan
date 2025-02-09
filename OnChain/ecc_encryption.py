from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt

class ECCEncryption:
    def __init__(self):
        eth_key = generate_eth_key()
        self.private_key = eth_key.to_hex()  # Private key in hex
        self.public_key = eth_key.public_key.to_hex()  # Public key in hex

    def encrypt_data(self, data):
        return encrypt(self.public_key, data.encode()).hex()

    def decrypt_data(self, encrypted_data, private_key_hex):
        """Decrypts data using the provided private key"""
        return decrypt(private_key_hex, bytes.fromhex(encrypted_data)).decode()

