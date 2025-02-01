import json
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

class Ecc:
    def __init__(self):
        """Initialize by generating a new ECC key pair."""
        self.private_key = ec.generate_private_key(ec.SECP256R1())
        self.public_key = self.private_key.public_key()

    def get_keys_as_json(self):
        """Return the ECC keys in JSON format for frontend storage."""
        private_int = self.private_key.private_numbers().private_value
        private_hex = hex(private_int)[2:]  # Convert to hex string

        public_numbers = self.public_key.public_numbers()
        public_x_hex = hex(public_numbers.x)[2:]
        public_y_hex = hex(public_numbers.y)[2:]
        public_hex = public_x_hex + public_y_hex  # Concatenate X and Y

        key_data = {
            "private_key": private_hex,
            "public_key": public_hex
        }
        return json.dumps(key_data)  # Convert to JSON and return

    @staticmethod
    def load_from_json(json_data):
        """Reconstruct ECC keys from JSON data received from frontend."""
        key_data = json.loads(json_data)

        # Convert hex to integer and restore private key
        private_int = int(key_data["private_key"], 16)
        private_key = ec.derive_private_key(private_int, ec.SECP256R1())

        # Split public key into X and Y
        public_x_hex = key_data["public_key"][:len(key_data["public_key"])//2]
        public_y_hex = key_data["public_key"][len(key_data["public_key"])//2:]
        public_x = int(public_x_hex, 16)
        public_y = int(public_y_hex, 16)

        # Restore public key
        public_key = ec.EllipticCurvePublicNumbers(public_x, public_y, ec.SECP256R1()).public_key()

        # Return a new instance with loaded keys
        instance = Ecc()
        instance.private_key = private_key
        instance.public_key = public_key
        return instance

    def sign_message(self, message):
        """Sign a message with the private key and return the signature."""
        signature = self.private_key.sign(message.encode(), ec.ECDSA(hashes.SHA256()))
        return signature.hex()  # Convert signature to hex string

    def verify_signature(self, message, signature_hex):
        """Verify a signature with the public key."""
        signature = bytes.fromhex(signature_hex)  # Convert hex back to bytes
        try:
            self.public_key.verify(signature, message.encode(), ec.ECDSA(hashes.SHA256()))
            return True  # Signature is valid
        except:
            return False  # Signature is invalid

