from OnChain.encoding import process_string
from OnChain.aes import AesEncryption
from OnChain.storeInfura import store_data_on_chainn
from OnChain.retriveInfura import get_data_from_transaction
from OnChain.decoding import decode_string

class Scheme1:
    def __init__(self, encryption_mode='CBC', encryption_size=256):
        self.aes = AesEncryption(mode=encryption_mode, size=encryption_size)
        self._password = "ppMan@Yourserv1c3"

    def encode_string(self, user_input):
        """Encodes a given string."""
        return process_string(user_input)

    def encrypt_data(self, data):
        """Encrypts data using AES encryption with a hardcoded password."""
        return self.aes.encrypt(data, password=self._password)

    def store_data_on_chain(self, encrypted_data):
        """Stores encrypted data on the blockchain."""
        return store_data_on_chainn(encrypted_data)

    def retrieve_data_from_chain(self, tx_hash):
        """Retrieves encrypted data from the blockchain using a transaction hash."""
        return get_data_from_transaction(tx_hash)

    def decrypt_data(self, encrypted_data):
        """Decrypts data using AES decryption with a hardcoded password."""
        decrypted_data = self.aes.decrypt(encrypted_data, password=self._password)
        return decrypted_data.decode('utf-8')

    def decode_string(self, encoded_string):
        """Decodes an encoded string back to its original form."""
        return decode_string(encoded_string)

# Example Usage:
if __name__ == "__main__":
    handler = Scheme1()

    # Step 1: Encode string
    user_input = "Feni@123"
    encoded_data = handler.encode_string(user_input)
    print(f"Encoded Data: {encoded_data}")

    # Step 2: Encrypt the encoded data
    encrypted_data = handler.encrypt_data(encoded_data)
    print(f"Encrypted Data: {encrypted_data}")

    # Step 3: Store encrypted data on blockchain
    tx_hash = handler.store_data_on_chain(encrypted_data)
    print(f"Transaction Hash: {tx_hash}")

    # Step 4: Retrieve encrypted data from blockchain
    retrieved_data = handler.retrieve_data_from_chain(tx_hash)
    print(f"Retrieved Encrypted Data: {retrieved_data}")

    # Step 5: Decrypt the data
    decrypted_data = handler.decrypt_data(encrypted_data)
    print(f"Decrypted Data: {decrypted_data}")

    # Step 6: Decode the original string
    original_string = handler.decode_string(decrypted_data)
    print(f"Original String: {original_string}")
