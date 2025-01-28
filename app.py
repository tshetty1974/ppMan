from flask import Flask, request, jsonify
from flask_cors import CORS
from Scheme1 import Scheme1  # Ensure the Scheme1 class is correctly imported

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow CORS globally

@app.route("/retrieve-password", methods=["POST"])
def retrieve_password():
    data = request.json
    tx_hash = data.get("transaction_hash")

    try:
        # Initialize Scheme1 instance
        handler = Scheme1()

        # Step 1: Retrieve encrypted data from blockchain
        encrypted_data = handler.retrieve_data_from_chain(tx_hash)

        # Step 2: Decrypt the data
        decrypted_password = handler.decrypt_data(encrypted_data)

        # Generate JSON response
        response_data = {"password": decrypted_password}

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/store-password", methods=["OPTIONS"])
def store_password_options():
    response = jsonify({"message": "CORS preflight successful"})
    response.headers.add("Access-Control-Allow-Origin", "chrome-extension://nemjagbapekbpfhbpokipfgghlkmalif")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response

@app.route("/store-password", methods=["POST"])
def store_password():
    data = request.json
    user_input = data.get("password")
    app_name = data.get("app")
    chain = data.get("chain")

    try:
        # Initialize Scheme1 instance
        handler = Scheme1()

        # Step 1: Encode string
        encoded_data = handler.encode_string(user_input)

        # Step 2: Encrypt the encoded data
        encrypted_data = handler.encrypt_data(encoded_data)

        # Step 3: Store encrypted data on blockchain
        tx_hash = handler.store_data_on_chain(encrypted_data)  # Actual transaction hash

        # Generate JSON response with the actual transaction hash
        response_data = {
            "transaction_hash": tx_hash,  # Actual hash from blockchain
            "chain": chain,
            "application/service": app_name,
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
