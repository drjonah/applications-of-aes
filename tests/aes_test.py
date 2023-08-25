# path to aes
import sys
sys.path.append('../applications-of-aes')

# packages
from aes import AES

## AES TESTS ##

plaintext = "Q2wE4rT6yU8iOpAs"

key128 = "ABCDEFGHIJKLMNOP"
key192 = "hwRhjC5s2YtACanDktuXKxte"
key256 = "w6HYstMa2dAxututGRaE2KPHdck9h9qg"

keys = [key128, key192, key256]

print("### AES TESTS ###")
print(f"Text = {plaintext}\n")

for key in keys:
    cipher = AES(key) # Key expansion
    print(f"Key = {key} ({len(key)})")

    encrypted = cipher.encrypt(plaintext) # Encyrpt
    print(f"Encrypted:\t{encrypted}")

    decrypted = cipher.decrypt(encrypted) # Decrypt
    print(f"Decrypted:\t{decrypted}\n")