import base64

def decode_part(encoded_part, scheme):
    try:
        if scheme == 1:  # Base64 Decoding
            return base64.b64decode(encoded_part.encode()).decode()
        elif scheme == 2:  # Hex Decoding
            return bytes.fromhex(encoded_part).decode()
        elif scheme == 3:  # Base85 Decoding
            return base64.a85decode(encoded_part.encode()).decode()
        else:
            raise ValueError("Invalid decoding scheme")
    except Exception as e:
        return base64.b64decode(encoded_part.encode()).decode()

def decode_string(encoded_string):
    encoded_parts = encoded_string.split("|")
    decoded_parts = []

    for i, part in enumerate(encoded_parts):
        if part:  # Only process non-empty parts
            scheme = (i % 3) + 1  # Scheme depends on the count of '|' passed (1-based index)
            try:
                decoded_parts.append(decode_part(part, scheme))
            except ValueError as e:
                print(f"Skipping problematic part: {part}. Error: {e}")

    # Combine all decoded parts
    original_string = "".join(decoded_parts)
    print(f"Decoded String: {original_string}")
    return original_string

# # Example usage
# # Assuming process_string is correctly defined
# encoded_string = "SGVsbA==|6f403132|Mw=="
# decode_string(encoded_string)