
from pathlib import Path
import sys
sys.path.append('../applications-of-aes') # path to aes

# local packages
from aes import AES
from apps.utils import load_encryption_key, load_chunks, record_time

def is_file(file_name: str) -> bool:
    """Ensures that the files exist."""
    return Path(file_name).is_file()

@record_time
def encrypt_file(aes: AES, file_in: str, file_out: str) -> bool:
    """Encrypts a .txt file and writes to a .bin file."""
    if not is_file(file_in) or not is_file(file_out):
        return False

    with open(file_in, "r") as FILE_READ:
        with open(file_out, "wb") as FILE_WRITE:
            for parse_line in FILE_READ.readlines():
                new_line = bytes()
                chunks = load_chunks(parse_line)

                for chunk in chunks: new_line += aes.encrypt(chunk)

                FILE_WRITE.write(new_line)

    return True

def decrypt_file(aes: AES, file_in: str, file_out: str) -> bool:
    """Decrypts a .bin file and writes to a .txt file."""
    if not is_file(file_in) or not is_file(file_out):
        return False

    with open(file_in, "rb") as FILE_READ:
        with open(file_out, "w") as FILE_WRITE:
            for parse_line in FILE_READ.readlines():
                new_line = str()
                chunks = load_chunks(parse_line)

                for chunk in chunks: new_line += aes.decrypt(chunk)

                FILE_WRITE.write(new_line)

    return True

def main(file_decoded_in: str, file_decoded_out: str, file_encoded_in: str, file_encoded_out: str, encrypt: bool) -> None:
    """Main function that handles arguments and produces output"""
    aes_key = load_encryption_key() # gets key from config.json for encryption
    aes = AES(aes_key) # creates AES object for encryption / decryption

    file_in, file_out = [file_decoded_in, file_encoded_out] if encrypt else [file_encoded_in, file_decoded_out]
    status = encrypt_file(aes, file_in, file_out) if encrypt else decrypt_file(aes, file_in, file_out)
    if status:
        print("File encryption success.") if encrypt else print("File decryption success.")
        print(f"Output of \"{file_in}\" found in \"{file_out}\"")
    else:
        print("Error converting file. Make sure that the file exist.")


if __name__ == "__main__":
    file_decoded_in = "./apps/textfiles/src/file_decoded_in.txt" # text file (input)
    file_decoded_out = "./apps/textfiles/src/file_decoded_out.txt" # text file (output)
    file_encoded_in = "./apps/textfiles/src/file_encoded_in.bin" # binary file (input)
    file_encoded_out = "./apps/textfiles/src/file_encoded_out.bin" # binary file (output)

    encrypt = False # true = encrypt file (file_decoded_in => file_encoded_out), false = decrypt file (file_encoded_in => file_decoded_out)

    main(file_decoded_in, file_decoded_out, file_encoded_in, file_encoded_out, encrypt)