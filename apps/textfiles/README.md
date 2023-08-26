# File Encryption and Decryption using AES

This repository contains a Python script that demonstrates file encryption and decryption using the Advanced Encryption Standard (AES) algorithm.

## Getting Started

### Prerequisites

Applications of AES repository (larger repository).

## Usage

1. **Configuration**: Before using the script, ensure that you have a valid encryption key stored in the `config.json` file. You can modify the `config.json` file to include your encryption key. The script uses this key for both encryption and decryption.

2. **File Paths**: Update the file paths in the script according to your file locations. You need to specify the input and output file paths for both plaintext and encrypted files. Modify the following variables in the script accordingly:

    ```
    file_text = "path/to/your/input/text/file_text.txt"
    file_binary = "path/to/your/input/binary/file_binary.bin"
    ```

3. **Encryption or Decryption**: Set the `encrypt` variable to `True` if you want to encrypt a plaintext file or `False` if you want to decrypt an encrypted binary file:

    ```
    encrypt = True  # Encrypt file (file_text.txt => file_text_output.bin)
    # OR
    encrypt = False  # Decrypt file (file_binary.bin => file_binary_output.txt)
    ```

4. **Run the Script**: Run the script using the following command:

    ```
    python script_name.py
    ```

    Replace `script_name.py` with the actual name of the Python script containing the provided code.

5. **Output**: After running the script, you will see the output indicating whether the file encryption/decryption was successful. The processed file will be saved with the appropriate output file extension.
