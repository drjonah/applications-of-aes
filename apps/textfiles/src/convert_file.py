
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
    with open(file_in, "rb") as FILE_READ:
        with open(file_out, "w") as FILE_WRITE:
            for parse_line in FILE_READ.readlines():
                new_line = str()
                chunks = load_chunks(parse_line)

                for chunk in chunks: new_line += aes.decrypt(chunk)

                FILE_WRITE.write(new_line)

    return True

def main(encrypt: bool, file: str, file_out=None) -> None:
    """Main function that handles arguments and produces output"""
    # optional param to specify existing output location, default is to create a new file
    assert is_file(file), "Specified input file does not exist."
    if file_out is None:
        file_out = file[:-4] + "_output." + ("bin" if encrypt else "txt") # creates path for file output
    else:
        assert is_file(file_out), "Specified output file does not exist."

    # creates AES object for encryption / decryption
    aes_key = load_encryption_key() # gets key from config.json for encryption
    aes = AES(aes_key)

    status = encrypt_file(aes, file, file_out) if encrypt else decrypt_file(aes, file, file_out)
    if status:
        print("File encryption success." if encrypt else "File decryption success.")
        print(f"Output of \"{file}\" found in \"{file_out}\"")
    else:
        print("Error converting file. Make sure that the file exist.")

if __name__ == "__main__":
    file_text = "apps/textfiles/src/file_text.txt" # text file (input)
    file_binary = "apps/textfiles/src/file_binary.bin" # binary file (input)
    encrypt = False # true = encrypt file (file_text.txt => file_text_out.bin), false = decrypt file (file_binary.bin => file_binary_out.txt)
    file = file_text if encrypt else file_binary # logic to decide file
    # main
    main(encrypt, file)