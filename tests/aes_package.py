import base64
from Crypto.Cipher import AES

def aes_encrypt(plaintext, key):
    plaintext = bytes(plaintext, "utf-8")
    key = bytes(key, "utf-8")
    padding_length = 16 - (len(plaintext) % 16)
    padded_plaintext = plaintext + bytes([padding_length] * padding_length)

    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(padded_plaintext)

    return base64.b64encode(ciphertext).decode('utf-8')    

plaintext = "a"
key = "TCw49FAk9CTAvzsd"

encrypt = aes_encrypt(plaintext, key)
print(encrypt)