from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

# Generate RSA keys
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Encrypt a message
def encrypt_message(message, public_key):
    ciphertext = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

# Decrypt a message
def decrypt_message(ciphertext, private_key):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode('utf-8')

# Save keys to PEM files
def save_keys_to_files(private_key, public_key):
    # Save private key
    with open("private_key.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )
    # Save public key
    with open("public_key.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

# Load keys from PEM files
def load_keys_from_files():
    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    with open("public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    return private_key, public_key

# Main function
if __name__ == "__main__":
    # Generate keys
    private_key, public_key = generate_keys()
    print("Keys generated.")

    # Save keys to files
    save_keys_to_files(private_key, public_key)
    print("Keys saved to files.")

    # Load keys from files
    private_key, public_key = load_keys_from_files()
    print("Keys loaded from files.")

    # Message to encrypt
    message = "This is a secret message."

    # Encrypt the message
    ciphertext = encrypt_message(message, public_key)
    print("Encrypted message:", ciphertext)

    # Decrypt the message
    decrypted_message = decrypt_message(ciphertext, private_key)
    print("Decrypted message:", decrypted_message)
