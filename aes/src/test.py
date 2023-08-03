import base64
from Crypto.Cipher import AES

def aes_encrypt(plaintext, key):
    # Pad the plaintext to be a multiple of 16 bytes (128 bits)
    # For simplicity, we'll use PKCS7 padding
    padding_length = 16 - (len(plaintext) % 16)
    padded_plaintext = plaintext + bytes([padding_length] * padding_length)

    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext

key = b"0" * 16  # The key should be in bytes format
plaintext = b"hello world"  # The plaintext should be in bytes format

ciphertext = aes_encrypt(plaintext, key)
base64_output = base64.b64encode(ciphertext).decode('utf-8')

print(f"Base64 Output: {base64_output}")
