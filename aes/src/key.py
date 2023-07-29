import secrets

# Generate a random 128-bit key (16 bytes)
key_size = 16
random_key = secrets.token_bytes(key_size)

# Convert the random key to a string (hexadecimal representation)
key = random_key.hex()

# Convert the hexadecimal representation to a string
key_string = str(key)

print("Random Key:", key_string)
