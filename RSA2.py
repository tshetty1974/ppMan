import json
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class RSA2:
    def __init__(self, key_size=2048):
        """Generate RSA keys."""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
        )
        self.public_key = self.private_key.public_key()

    def get_keys_as_json(self):
        """Return RSA keys in JSON format for frontend storage."""
        private_numbers = self.private_key.private_numbers()

        # Convert private key components to hex
        private_d = hex(private_numbers.d)[2:]
        private_n = hex(private_numbers.public_numbers.n)[2:]
        private_e = hex(private_numbers.public_numbers.e)[2:]

        # Convert public key components to hex
        public_n = private_n
        public_e = private_e

        key_data = {
            "private_key": {
                "d": private_d,
                "n": private_n,
                "e": private_e
            },
            "public_key": {
                "n": public_n,
                "e": public_e
            }
        }
        return json.dumps(key_data)  # Convert to JSON and return

    @staticmethod
    def load_from_json(json_data):
        """Reconstruct RSA keys from JSON data received from frontend."""
        key_data = json.loads(json_data)

        # Convert hex values back to integers
        d = int(key_data["private_key"]["d"], 16)
        n = int(key_data["private_key"]["n"], 16)
        e = int(key_data["private_key"]["e"], 16)

        # Restore private key
        private_numbers = rsa.RSAPrivateNumbers(
            p=None,  # Auto-generate
            q=None,  # Auto-generate
            d=d,
            dmp1=None,
            dmq1=None,
            iqmp=None,
            public_numbers=rsa.RSAPublicNumbers(e, n)
        )
        private_key = private_numbers.private_key()

        # Restore public key
        public_numbers = rsa.RSAPublicNumbers(e, n)
        public_key = public_numbers.public_key()

        # Return an instance with restored keys
        instance = RSA2()
        instance.private_key = private_key
        instance.public_key = public_key
        return instance

    def encrypt_message(self, message):
        """Encrypt a message with the public key."""
        ciphertext = self.public_key.encrypt(
            message.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext.hex()  # Convert bytes to hex for JSON storage

    def decrypt_message(self, ciphertext_hex):
        """Decrypt a message with the private key."""
        ciphertext = bytes.fromhex(ciphertext_hex)  # Convert hex back to bytes
        plaintext = self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext.decode("utf-8")
