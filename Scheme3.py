from OnChain.ecc_encryption import ECCEncryption
from OnChain.storeInfura import store_data_on_chainn
from OnChain.retriveInfura import get_data_from_transaction

class Scheme3:
    def __init__(self):
        self.ecc = ECCEncryption()

    def encrypt_data(self, data):
        return self.ecc.encrypt_data(data)

    def store_data_on_chain(self, encrypted_data):
        return store_data_on_chainn(encrypted_data)

    def retrieve_data_from_chain(self, tx_hash):
        return get_data_from_transaction(tx_hash)

    def decrypt_data(self, encrypted_data, private_key):
        return self.ecc.decrypt_data(encrypted_data, private_key)

