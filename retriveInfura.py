from web3 import Web3
import os

# Function to retrieve binary data from a transaction hash
def get_data_from_transaction(tx_hash):
    # Load environment variables
    INFURA_URL = os.getenv("INFURA_URL")

    if not INFURA_URL:
        raise ValueError("Ensure INFURA_URL is set as an environment variable.")

    # Connect to the Sepolia network
    web3 = Web3(Web3.HTTPProvider(INFURA_URL))
    if not web3.is_connected():
        raise ConnectionError("Failed to connect to Sepolia network.")

    # Get the transaction details
    try:
        tx_receipt = web3.eth.get_transaction(tx_hash)
    except Exception as e:
        raise ValueError(f"Failed to fetch transaction details: {e}")

    # Extract the data field
    hex_data = tx_receipt.get("input", None)
    if not hex_data:
        raise ValueError("No data found in the transaction.")

    # # Convert hex data back to binary
    # if isinstance(hex_data, bytes):
    #     hex_data = hex_data.hex()  # Convert HexBytes to string if needed
    binary_data = Web3.to_bytes(hexstr=hex_data)

    print(f"Retrieved Binary Data: {binary_data}")
    return binary_data

# Example Usage
if __name__ == "__main__":
    # Replace with the transaction hash you want to retrieve data from
    transaction_hash = "0x235c4909c980b2acfc3b58b2c29eafe7e98d301160ba3e43eb741a3a441db4d4"

    try:
        original_binary_data = get_data_from_transaction(transaction_hash)
        print(f"Original Binary Data: {original_binary_data}")
    except Exception as e:
        print(f"Error: {e}")
