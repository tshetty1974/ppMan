import base64

def encode_part(part, scheme):
    if scheme == 1:  # Base64 Encoding
        return base64.b64encode(part.encode()).decode()
    elif scheme == 2:  # Hex Encoding
        return part.encode().hex()
    elif scheme == 3:  # Base85 Encoding
        return base64.a85encode(part.encode()).decode()  
    else:
        raise ValueError("Invalid encoding scheme")

def process_string(user_input):
    length = len(user_input)
    print(f"Original String: {user_input}")
    print(f"Length of String: {length}")

    # Divide length by 4
    num_parts = length // 4
    remainder = length % 4

    encoded_parts = []

    # Encode each part
    for i in range(num_parts):
        part = user_input[i * 4: (i + 1) * 4]  # Get 4-character segment
        scheme = (i % 3) + 1  # Cycle through schemes: 1, 2, 3
        encoded_parts.append(encode_part(part, scheme))

    # Handle remainder
    if remainder > 0:
        remaining_part = user_input[-remainder:]  # Last few characters
        encoded_parts.append(encode_part(remaining_part, 1))  # Use scheme 1 for remainder

    # Combine all encoded parts
    encoded_string = "|".join(encoded_parts)
    print(f"Encoded String: {encoded_string}")
    return encoded_string
