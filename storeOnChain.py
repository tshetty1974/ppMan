from web3 import Web3
import os

# Function to store binary data (encrypted) on-chain
def store_data_on_chain(binary_data):
    # Load environment variables
    JSON_RPC_URL = os.getenv("JSON_RPC_URL")  # Replace with your JSON-RPC URL
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")

    if not JSON_RPC_URL or not PRIVATE_KEY:
        raise ValueError("Ensure JSON_RPC_URL and PRIVATE_KEY are set as environment variables.")

    # Connect to the Ethereum network using JSON-RPC
    web3 = Web3(Web3.HTTPProvider(JSON_RPC_URL))
    if not web3.is_connected():
        raise ConnectionError("Failed to connect to Ethereum network using JSON-RPC.")

    # Derive the sender's address from the private key
    account = web3.eth.account.from_key(PRIVATE_KEY)
    sender_address = account.address
    print(f"Connected to Ethereum. Sender Address: {sender_address}")

    # Convert binary data to hex format
    hex_data = Web3.to_hex(binary_data)  # Converts binary to hex string

    # Get the current nonce for the sender address
    nonce = web3.eth.get_transaction_count(sender_address)

    # Build the transaction
    transaction = {
        "from": sender_address,
        "to": sender_address,  # Change as needed
        "value": 0,  # No ETH transferred
        "gas": 300000,
        "gasPrice": web3.to_wei("10", "gwei"),
        "nonce": nonce,
        "data": hex_data,
        'chainId': web3.eth.chain_id,
    }

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, PRIVATE_KEY)

    # Send the signed transaction
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        print(f"Transaction sent successfully! Hash: {web3.to_hex(tx_hash)}")
        return web3.to_hex(tx_hash)  # Return the transaction hash
    except Exception as e:
        raise RuntimeError(f"Failed to send transaction: {e}")

# Example Usage
if __name__ == "__main__":
    # Example encrypted binary message
    encrypted_message = b'\x48\x65\x6c\x6c\x6f\x2c\x20\x45\x74\x68\x65\x72\x65\x75\x6d'  # Binary data
    transaction_hash = store_data_on_chain(encrypted_message)
    print(f"Transaction Hash: {transaction_hash}")


