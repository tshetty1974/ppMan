import logging
from OnChain.encoding import process_string
from kyber.pywrapper.encryption import generate_keypair, encapsulate, decapsulate
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Set up logging
logging.basicConfig(level=logging.INFO)

def binary_conversion(data):
    """Convert the entire string (including '|') into binary."""
    return ''.join(format(ord(char), '08b') for char in data)

def binary_to_string(binary_data):
    """Convert binary back to the original string (with '|')."""
    return ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))

def aes_encrypt(data, key):
    """Encrypt the data using AES with the shared secret as the key."""
    try:
        cipher = AES.new(key[:16], AES.MODE_CBC)  # Use the first 16 bytes of the key
        ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))
        return base64.b64encode(cipher.iv + ciphertext).decode()
    except Exception as e:
        logging.error(f"AES encryption failed: {e}")
        raise

def aes_decrypt(data, key):
    """Decrypt the data using AES with the shared secret as the key."""
    try:
        raw_data = base64.b64decode(data)
        iv = raw_data[:16]
        ciphertext = raw_data[16:]
        cipher = AES.new(key[:16], AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext.decode()
    except Exception as e:
        logging.error(f"AES decryption failed: {e}")
        raise

def encode_and_encrypt(user_input):
    try:
        # Encode the input
        encoded_string = process_string(user_input)
        logging.info(f"Encoded String: {encoded_string}")

        # Convert to binary
        binary_data = binary_conversion(encoded_string)
        logging.info(f"Binary Data: {binary_data}")

        # Generate Kyber keys
        public_key, private_key = generate_keypair()
        logging.info(f"Public Key: {public_key}")
        logging.info(f"Private Key: {private_key}")

        # Encapsulate the shared secret using Kyber
        ciphertext, shared_secret = encapsulate(public_key)
        logging.info(f"Ciphertext (Kyber): {ciphertext}")
        logging.info(f"Shared Secret: {shared_secret}")

        # Encrypt the binary data with AES using the shared secret
        encrypted_binary_data = aes_encrypt(binary_data, shared_secret)
        logging.info(f"Encrypted Binary Data: {encrypted_binary_data}")

        return encrypted_binary_data, ciphertext, private_key
    except Exception as e:
        logging.error(f"Encode and Encrypt failed: {e}")
        raise

def decrypt_and_decode(encrypted_binary_data, ciphertext, private_key):
    try:
        # Decapsulate the shared secret
        recovered_secret = decapsulate(ciphertext, private_key)
        logging.info(f"Recovered Shared Secret: {recovered_secret}")

        # Decrypt the binary data
        decrypted_binary_data = aes_decrypt(encrypted_binary_data, recovered_secret)
        logging.info(f"Decrypted Binary Data: {decrypted_binary_data}")

        # Convert binary back to string
        decoded_string = binary_to_string(decrypted_binary_data)
        logging.info(f"Decoded String: {decoded_string}")

        # Split and decode parts
        parts = decoded_string.split('|')
        decoded_parts = []
        for part in parts:
            try:
                # Decode as hex if possible
                decoded_parts.append(bytes.fromhex(part).decode())
            except ValueError:
                # Otherwise, treat as ASCII
                decoded_parts.append(part)

        logging.info(f"Decoded Parts: {decoded_parts}")
        return decoded_parts
    except Exception as e:
        logging.error(f"Decrypt and Decode failed: {e}")
        raise
