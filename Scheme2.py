import base64
import binascii
from OnChain.rsa_encryption import RSAEncryption
from OnChain.storeInfura import store_data_on_chainn
from OnChain.retriveInfura import get_data_from_transaction

class Scheme2:
    def __init__(self):
        self.rsa = RSAEncryption()

    def encrypt_data(self, data):
        """Encrypts data with RSA and converts Base64 to Hex before storing."""
        encrypted_base64 = self.rsa.encrypt(data)  # RSA encryption gives Base64
        encrypted_hex = binascii.hexlify(base64.b64decode(encrypted_base64)).decode()  # Convert Base64 → Hex

        return {
            "encrypted_data": encrypted_hex,  # Store only Hex on blockchain
            "public_key": self.rsa.public_key.decode(),
            "private_key": self.rsa.private_key.decode()
        }

    def store_data_on_chain(self, encryption_result):
        """Stores only the encrypted Hex data on the blockchain."""
        encrypted_hex = encryption_result["encrypted_data"]  #  Extract only the encrypted hex
        return store_data_on_chainn(encrypted_hex)  # Store only encrypted hex, not full dict

    def retrieve_data_from_chain(self, tx_hash):
        """Retrieves data from blockchain and ensures it's in the correct format for decryption."""
        encrypted_data = get_data_from_transaction(tx_hash)  # Retrieve stored data
        
        # Fix: If data is bytes, convert it to hex before decoding
        if isinstance(encrypted_data, bytes):  
            encrypted_hex = encrypted_data.hex()  # Convert bytes to hex
        else:
            encrypted_hex = encrypted_data  # If already hex, keep as is

        encrypted_base64 = base64.b64encode(binascii.unhexlify(encrypted_hex)).decode()  # Convert Hex → Base64
        return encrypted_base64  # Return Base64 for decryption

    def decrypt_data(self, encrypted_data, private_key):
        """Decrypts the Base64 data using RSA private key."""
        return self.rsa.decrypt(encrypted_data, private_key)  # Normal RSA decryption
