import os
from encoding import process_string
from aes import AesEncryption
from storeInfura import store_data_on_chainn
from retriveInfura import get_data_from_transaction
from decoding import decode_string

# Step 1: Input String and Encode
user_input = "Feni@123"
encoded_data = process_string(user_input)
print(f"Encoded Data: {encoded_data}")

# Step 2: Encrypt Encoded Data
password = "Manny@123"  # Replace with a strong password
aes = AesEncryption(mode='CBC', size=256)  # Initialize AES encryption
encrypted_data = aes.encrypt(encoded_data, password=password)
print(f"Encrypted Data: {encrypted_data}")

# Step 3: Store Encrypted Data on Blockchain
tx_hash = store_data_on_chainn(encrypted_data)
print(f"Transaction Hash: {tx_hash}")

# Step 4: Retrieve Encrypted Data from Blockchain
retrieved_encrypted_data = get_data_from_transaction(tx_hash)
print(f"Retrieved Encrypted Data: {retrieved_encrypted_data}")

# Step 5: Decrypt the Data
decrypted_data = aes.decrypt(encrypted_data, password=password)
print(f"Decrypted Data: {decrypted_data}")
original_string = decrypted_data.decode('utf-8')
print(f"original_string:{original_string}")

#Srep 6 decoding 
print(decode_string(original_string))

