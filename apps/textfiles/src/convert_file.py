
from pathlib import Path
import sys
sys.path.append('../applications-of-aes') # path to aes

# local packages
from aes import AES
from apps.utils import load_encryption_key, load_chunks

def is_file(file_name: str) -> bool:
    """Ensures that the files exist."""
    return Path(file_name).is_file()

def encrypt_file(aes: AES, file_in: str, file_out: str) -> bool:
    """Encrypts a .txt file and writes to a .bin file."""
    with open(file_in, "r") as FILE_READ: # reads txt file
        with open(file_out, "wb") as FILE_WRITE: # writes bin file
            for parse_line in FILE_READ.readlines(): # iterate through txt file
                new_line = bytes() # variable that is written to bin file
                chunks = load_chunks(parse_line) # splits the line into chunks

                for chunk in chunks: new_line += aes.encrypt(chunk) # encrypts the chunks

                FILE_WRITE.write(new_line) # writes the encrypted line

    return True

def decrypt_file(aes: AES, file_in: str, file_out: str) -> bool:
    """Decrypts a .bin file and writes to a .txt file."""
    with open(file_in, "rb") as FILE_READ: # reads bin file
        with open(file_out, "w") as FILE_WRITE: # writes txt file
            # loop that reads the binary file and decrypts it on chunks of 16 bytes
            while True:
                chunk = FILE_READ.read(16) # reads 16 bytes at a time
                if not chunk: # breaks when there are no more cunks 
                    break
                FILE_WRITE.write(aes.decrypt(chunk)) # writes decrypted chunks to txt file 

    return True

def main(file: str, file_out=None) -> None:
    """Main function that handles arguments and produces output"""
    assert is_file(file), "Specified input file does not exist."
    assert file[-3:] in ["txt", "bin"], "Incorrect file type. [txt, bin]"

    encrypt = True if file[-3:] == "txt" else False # encrypts if it is a text file, decrypts if it is a bin

    # optional param to specify existing output location, default is to create a new file
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
    file = "apps/textfiles/src/file_text.txt" # text file to encrypt
    # file = "apps/textfiles/src/file_binary.bin" # text file to decrypt

    main(file) # main method