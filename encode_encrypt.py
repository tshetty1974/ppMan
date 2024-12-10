from encoding import process_string
from kyber.pywrapper.encryption import generate_keypair, encapsulate, decapsulate
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

#def binary_coversion(user_input)
        ##logic to be written
        #return binary_data 
def aes_encrypt(data, key):
    """Encrypt the data using AES with the shared secret as the key."""
    cipher = AES.new(key[:16], AES.MODE_CBC)  # Use the first 16 bytes of the key
    ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(cipher.iv + ciphertext).decode()

def aes_decrypt(data, key):
    """Decrypt the data using AES with the shared secret as the key."""
    raw_data = base64.b64decode(data)
    iv = raw_data[:16]
    ciphertext = raw_data[16:]
    cipher = AES.new(key[:16], AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

def encode_and_encrypt(user_input):
    # Encode the input
    encoded_string = process_string(user_input)
    print(f"Encoded String: {encoded_string}")

    # Generate Kyber keys
    public_key, private_key = generate_keypair()
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")

    # Encapsulate the shared secret using Kyber
    ciphertext, shared_secret = encapsulate(public_key)
    print(f"Ciphertext (Kyber): {ciphertext}")
    print(f"Shared Secret: {shared_secret}")

    # Encrypt the encoded string with AES using the shared secret
    encrypted_encoded_string = aes_encrypt(encoded_string, shared_secret)
    print(f"Encrypted Encoded String: {encrypted_encoded_string}")

    # Decapsulate the shared secret (for demonstration)
    recovered_secret = decapsulate(ciphertext, private_key)
    print(f"Recovered Shared Secret: {recovered_secret}")

    # Verify the shared secret matches
    assert shared_secret == recovered_secret, "Shared secrets do not match!"

    # Decrypt the encoded string using the recovered shared secret
    decrypted_encoded_string = aes_decrypt(encrypted_encoded_string, recovered_secret)
    print(f"Decrypted Encoded String: {decrypted_encoded_string}")

    # Verify the decrypted encoded string matches the original encoded string
    assert decrypted_encoded_string == encoded_string, "Decrypted encoded string does not match the original!"
    print("Encoding, encryption, and decryption successful!")
    return encrypted_encoded_string

# Example usage
if __name__ == "__main__":
    user_input = input("Enter a string to encode and encrypt: ")
    #binay_data=binary_conversion(user_input)
    #encode_and_encrypt(binary_data)
