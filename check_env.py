import os

# Fetch environment variables
infura_url = os.getenv("INFURA_URL")
private_key = os.getenv("PRIVATE_KEY")

# Check if the variables are accessible
if not infura_url or not private_key:
    raise ValueError("Environment variables not set correctly!")

print("INFURA_URL:", infura_url)
print("PRIVATE_KEY:", private_key[:10] + "..." + private_key[-5:])  # Mask private key for security
