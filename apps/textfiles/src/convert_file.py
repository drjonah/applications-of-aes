
from pathlib import Path
import sys
sys.path.append('../applications-of-aes') # path to aes

# local packages
from aes import AES
from apps.utils import load_encryption_settings

def is_file(file_name: str) -> bool:
    """Ensures that the files exist."""
    return Path(file_name).is_file()

def encrypt_file(args: list, file_in: str, file_out: str) -> bool:
    """Encrypts a .txt file and writes to a .bin file."""
    aes, cbc, iv = args
    with open(file_in, "r") as FILE_READ: # reads txt file
        with open(file_out, "wb") as FILE_WRITE: # writes bin file
            # write cbc differently than ecb because of the iv
            if cbc:
                try:
                    FILE_WRITE.write(aes.encrypt(FILE_READ.read(), cbc, iv)) # writes the encrypted line
                except Exception as e:
                    print(f"Encryption error: {e}")
                    return False # ECB works as one string so all fails
            else:
                for parse_line in FILE_READ.readlines(): # iterate through txt file
                    try:
                        new_line = aes.encrypt(parse_line)
                        FILE_WRITE.write(new_line) # writes the encrypted line
                    except Exception as e:
                        print(f"Encryption error: {e}")
    return True

def decrypt_file(args: list, file_in: str, file_out: str) -> bool:
    """Decrypts a .bin file and writes to a .txt file."""
    aes, cbc, iv = args
    with open(file_in, "rb") as FILE_READ: # reads bin file
        with open(file_out, "w") as FILE_WRITE: # writes txt file
            # read cbc differently than ecb because of iv   
            if cbc:
                try:
                    FILE_WRITE.write(aes.decrypt(FILE_READ.read(), cbc, iv)) # writes decrypted chunks to txt file 
                except Exception as e:
                    print(f"Decryption error: {e}") 
                    return False # ECB works as one string so all fails
            else:
                # loop that reads the binary file and decrypts it on chunks of 16 bytes
                while True:
                    chunk = FILE_READ.read(16) # reads 16 bytes at a time
                    if not chunk: # breaks when there are no more cunks 
                        break
                    try:
                        FILE_WRITE.write(aes.decrypt(chunk))
                    except Exception as e:
                        print(f"Decryption error: {e}")
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
    aes_key, cbc, iv = load_encryption_settings() # gets key from config.json for encryption
    aes = AES(aes_key)

    args = [aes, cbc, iv]

    status = encrypt_file(args, file, file_out) if encrypt else decrypt_file(args, file, file_out)
    if status:
        print("File encryption success." if encrypt else "File decryption success.")
        print(f"Output of \"{file}\" found in \"{file_out}\"")
    else:
        print("Error converting file. Make sure that the file exist.")


if __name__ == "__main__":
    # NOTE: Decryption erros are often due to CBC 
    #   1. Unmatching IV used in encryption
    #   2. Decrypting in ECB when it was encrypted in CBC

    # file = "apps/textfiles/data/file_text_ecb.txt" # text file to encrypt (ECB)
    # file = "apps/textfiles/data/file_text_ecb_output.bin" # text file to dencrypt (ECB)
    # file = "apps/textfiles/data/file_text_cbc.txt" # text file to encrypt (CBC)
    file = "apps/textfiles/data/file_text_cbc_output.bin" # text file to decrypt (CBC)
    main(file) # main method