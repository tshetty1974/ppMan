from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2, HKDF
from Crypto.Hash import HMAC, SHA256, SHA512
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from web3 import Web3
import base64
import os

class EncryptionScheme:
    def __init__(self, mode='CBC', key_size=128):
        self.aes_mode = {'CBC': AES.MODE_CBC, 'CFB': AES.MODE_CFB}
        self.key_sizes = (128, 192, 256)
        if mode not in self.aes_mode:
            raise ValueError("Unsupported AES mode.")
        if key_size not in self.key_sizes:
            raise ValueError("Unsupported key size.")

        self.mode = mode
        self.key_size = key_size // 8
        self.master_key = None
        self.salt_len = 16
        self.iv_len = 16
        self.mac_len = 32
        self.base64 = True

    def set_master_key(self, key):
        self.master_key = base64.b64decode(key) if isinstance(key, str) else key

    def random_key_gen(self):
        self.master_key = get_random_bytes(self.key_size)
        return base64.b64encode(self.master_key).decode()

    def _derive_keys(self, salt, password=None):
        if password:
            dkey = PBKDF2(password, salt, self.key_size + self.mac_len, count=20000, hmac_hash_module=SHA512)
        elif self.master_key:
            dkey = HKDF(self.master_key, self.key_size + self.mac_len, salt, SHA256)
        else:
            raise ValueError("No password or master key provided.")

        return dkey[:self.key_size], dkey[self.key_size:]

    def encrypt(self, data, password=None):
        salt = get_random_bytes(self.salt_len)
        iv = get_random_bytes(self.iv_len)
        aes_key, mac_key = self._derive_keys(salt, password)

        cipher = AES.new(aes_key, self.aes_mode[self.mode], iv)
        ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))
        mac = HMAC.new(mac_key, iv + ciphertext, digestmod=SHA256).digest()

        encrypted_data = salt + iv + ciphertext + mac
        return base64.b64encode(encrypted_data).decode()

    def decrypt(self, encrypted_data, password=None):
        encrypted_data = base64.b64decode(encrypted_data)
        salt = encrypted_data[:self.salt_len]
        iv = encrypted_data[self.salt_len:self.salt_len + self.iv_len]
        ciphertext = encrypted_data[self.salt_len + self.iv_len:-self.mac_len]
        mac = encrypted_data[-self.mac_len:]

        aes_key, mac_key = self._derive_keys(salt, password)
        HMAC.new(mac_key, iv + ciphertext, digestmod=SHA256).verify(mac)

        cipher = AES.new(aes_key, self.aes_mode[self.mode], iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext.decode()

    @staticmethod
    def encode(data, scheme):
        if scheme == 1:
            return base64.b64encode(data.encode()).decode()
        elif scheme == 2:
            return data.encode().hex()
        elif scheme == 3:
            return base64.a85encode(data.encode()).decode()
        else:
            raise ValueError("Invalid encoding scheme.")

    @staticmethod
    def decode(encoded_data, scheme):
        if scheme == 1:
            return base64.b64decode(encoded_data).decode()
        elif scheme == 2:
            return bytes.fromhex(encoded_data).decode()
        elif scheme == 3:
            return base64.a85decode(encoded_data).decode()
        else:
            raise ValueError("Invalid decoding scheme.")

    @staticmethod
    def process_string(user_input):
        length = len(user_input)
        num_parts = length // 4
        remainder = length % 4

        encoded_parts = []
        for i in range(num_parts):
            part = user_input[i * 4: (i + 1) * 4]
            scheme = (i % 3) + 1
            encoded_parts.append(EncryptionScheme.encode(part, scheme))

        if remainder > 0:
            remaining_part = user_input[-remainder:]
            encoded_parts.append(EncryptionScheme.encode(remaining_part, 1))

        return "|".join(encoded_parts)

    @staticmethod
    def decode_string(encoded_string):
        encoded_parts = encoded_string.split("|")
        decoded_parts = []

        for i, part in enumerate(encoded_parts):
            if part:
                scheme = (i % 3) + 1
                try:
                    decoded_parts.append(EncryptionScheme.decode(part, scheme))
                except Exception as e:
                    print(f"Skipping problematic part: {part}. Error: {e}")

        return "".join(decoded_parts)

    @staticmethod
    def store_on_blockchain(binary_data):
        infura_url = os.getenv("INFURA_URL")
        private_key = os.getenv("PRIVATE_KEY")
        if not infura_url or not private_key:
            raise ValueError("Set INFURA_URL and PRIVATE_KEY in environment variables.")

        web3 = Web3(Web3.HTTPProvider(infura_url))
        if not web3.is_connected():
            raise ConnectionError("Failed to connect to the blockchain.")

        account = web3.eth.account.from_key(private_key)
        nonce = web3.eth.get_transaction_count(account.address)

        tx = {
            "from": account.address,
            "to": "0xRecipientAddress",  # Replace with recipient address
            "value": 0,
            "gas": 23050,
            "gasPrice": web3.to_wei("10", "gwei"),
            "nonce": nonce,
            "data": binary_data
        }

        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return web3.to_hex(tx_hash)

    @staticmethod
    def retrieve_from_blockchain(tx_hash):
        infura_url = os.getenv("INFURA_URL")
        if not infura_url:
            raise ValueError("Set INFURA_URL in environment variables.")

        web3 = Web3(Web3.HTTPProvider(infura_url))
        if not web3.is_connected():
            raise ConnectionError("Failed to connect to the blockchain.")

        tx_receipt = web3.eth.get_transaction(tx_hash)
        return tx_receipt.input
