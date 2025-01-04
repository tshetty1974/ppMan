from web3 import Web3
import os

def retrieve_data_from_chain(tx_hash):
    # Load environment variables
    JSON_RPC_URL = os.getenv("JSON_RPC_URL")  # Replace with your JSON-RPC URL

    if not JSON_RPC_URL:
        raise ValueError("Ensure JSON_RPC_URL is set as an environment variable.")

    # Connect to the Ethereum network using JSON-RPC
    web3 = Web3(Web3.HTTPProvider(JSON_RPC_URL))
    if not web3.is_connected():
        raise ConnectionError("Failed to connect to Ethereum network using JSON-RPC.")

    try:
        # Fetch the transaction using the transaction hash
        transaction = web3.eth.get_transaction(tx_hash)
    except Exception as e:
        raise ValueError(f"Failed to fetch transaction: {e}")

    # Extract the `input` field (data field) from the transaction
    input_data = transaction.get('input')
    if not input_data or input_data == "0x":
        raise ValueError("No data embedded in this transaction.")

    # Decode the hex data back to binary
    binary_data = Web3.toBytes(hexstr=input_data)
    print(f"Retrieved Binary Data: {binary_data}")
    return binary_data

# Example Usage
if __name__ == "__main__":
    # Example transaction hash (replace with your actual hash)
    tx_hash = "0xYourTransactionHashHere"  # Replace with the hash returned during storage
    retrieved_data = retrieve_data_from_chain(tx_hash)
    print(f"Retrieved Data: {retrieved_data}")
