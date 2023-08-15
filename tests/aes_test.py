import sys
sys.path.append('../applications-of-aes')

from aes import AES

## AES TESTS ##
print("### AES EXECUTION ###")

plaintext = "a"
key = "ABCDEFGHIJKLMNOP"

cipher128 = AES(key)
encrypted = cipher128.encrypt(plaintext)
decrypted = cipher128.decrypt(encrypted)

# cipher192 = AES("hwRhjC5s2YtACanDktuXKxte")
# encrypted = cipher192.encrypt("hello world")
# encrypted = cipher192.decrypt("hello world")

# cipher256 = AES("w6HYstMa2dAxututGRaE2KPHdck9h9qg")
# encrypted = cipher256.encrypt("hello world")
# encrypted = cipher256.decrypt("hello world")

print("### AES TESTS ###")
print(f"Information:\n\tKey = {key}\n\tText = {plaintext}")
print(f"Encrypted:\t{encrypted}")
print(f"Decrypted:\t{decrypted}")