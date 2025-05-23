from web3 import Web3
import os

# Function to store binary data (encrypted) on-chain
def store_data_on_chainn(binary_data):
   
    # Load environment variables
    INFURA_URL = os.getenv("INFURA_URL")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")

    if not INFURA_URL or not PRIVATE_KEY:
        raise ValueError("Ensure INFURA_URL and PRIVATE_KEY are set as environment variables.")

    # Connect to the Sepolia network
    web3 = Web3(Web3.HTTPProvider(INFURA_URL))
    if not web3.is_connected():
        raise ConnectionError("Failed to connect to Sepolia network.")

    # Derive the sender's address from the private key
    account = web3.eth.account.from_key(PRIVATE_KEY)
    sender_address = account.address
    print(f"Connected to Sepolia. Sender Address: {sender_address}")

    balance = web3.eth.get_balance(sender_address)
    print(f"Sender Balance: {web3.from_wei(balance, 'ether')} ETH")

    print(f"hey i am storeInfura before putting in blockchain:{binary_data}")

    # # Convert binary data to hex format
    # hex_data = Web3.to_hex(binary_data)  # Converts binary to hex string

    # Get the current nonce for the sender address
    nonce = web3.eth.get_transaction_count(sender_address)

    # Build the transaction
    transaction = {
        "from": sender_address,
        "to": "0xC2996213e5D2e9F314892B089B7B4F27e54e50cE",  
        "value": 0,  # No ETH transferred
        "gas": 23050,  
        "gasPrice": web3.to_wei("10", "gwei"),  
        "nonce": nonce,
        "data": binary_data, 
    }

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, PRIVATE_KEY)

    # Send the signed transaction
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"Transaction sent successfully! Hash: {web3.to_hex(tx_hash)}")

    return web3.to_hex(tx_hash)  # Return the transaction hash

# # Example Usage
# if __name__ == "__main__":
#     # Example encrypted binary message
#     encrypted_message = b'\x48\x65\x6c\x6c\x6f\x2c\x20\x45\x74\x68\x65\x72\x65\x75\x7d'  # Binary data
#     transaction_hash = store_data_on_chainn(encrypted_message)
#     print(f"Transaction Hash: {transaction_hash}")