import base64
from rijndael import RCON, SBOX, SBOX_INV

# http://cs.ucsb.edu/~koc/cs178/projects/JT/aes.c
xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

## TOOLS ##
def to_matrix(block: list) -> list:
    """Convert a 16-byte block to a 4x4 matrix."""
    return [list(block[index:index+4]) for index in range(0, len(block), 4)]

def to_bytes(block: list) -> bytes:
    """Convert a 4x4 matrix to a 16-byte block."""
    return bytes(sum(block, []))

def pkcs7_padding(data: bytes, block_size: int) -> bytes:
    """Apply PKCS#7 padding to the data to make it a multiple of block_size."""
    padding_length = block_size - len(data) % block_size
    padding = bytes([padding_length] * padding_length)
    return data + padding

def pkcs7_padding_undo():
    pass

## ENCRYPTION ##
def sub_bytes(block: list) -> list:
    """Apply SubBytes transformation to the block."""
    results = [SBOX[b] for b in block]

    return results

def sub_bytes_inv(block: list) -> list:
    """Apply SubBytes inverse transformation to the block."""
    results = [SBOX_INV[b] for b in block]

    return results

def rot_bytes(block: list) -> list:
    """Rotate the bytes in the block to the left by one position."""
    return block[1:] + block[:1]

def shift_rows(block: list) -> list:
    """Shift the rows in the block according to AES specifications."""
    block[1] = [block[1][(i + 1) % 4] for i in range(4)] # row 1 shifts 1
    block[2] = [block[2][(i + 2) % 4] for i in range(4)] # row 2 shifts 2
    block[3] = [block[3][(i + 3) % 4] for i in range(4)] # row 3 shifts 3

def shift_rows_inverse(block: list) -> list:
    """Inverse ShiftRows transformation for decryption."""
    block[1] = [block[1][(i - 1) % 4] for i in range(4)]  # row 1 shifts 1 position to the right
    block[2] = [block[2][(i - 2) % 4] for i in range(4)]  # row 2 shifts 2 positions to the right
    block[3] = [block[3][(i - 3) % 4] for i in range(4)]  # row 3 shifts 3 positions to the right

def mix_columns(block: list) -> list:
    """Apply MixColumns transformation to a single column of the block."""
    for index in range(0, len(block)):
        t = block[index][0] ^ block[index][1] ^ block[index][2] ^ block[index][3]
        u = block[index][0]
        block[index][0] ^= t ^ xtime(block[index][0] ^ block[index][1])
        block[index][1] ^= t ^ xtime(block[index][1] ^ block[index][2])
        block[index][2] ^= t ^ xtime(block[index][2] ^ block[index][3])
        block[index][3] ^= t ^ xtime(block[index][3] ^ u)

def mix_columns_inverse(block: list) -> list:
    """Apply MixColumns inverse transformation to a single column of the block."""
    for i in range(4):
        u = xtime(xtime(block[i][0] ^ block[i][2]))
        v = xtime(xtime(block[i][1] ^ block[i][3]))
        block[i][0] ^= u
        block[i][1] ^= v
        block[i][2] ^= u
        block[i][3] ^= v

    mix_columns(block)

def add_round(block: list, key: list):
    """Apply AddRoundKey transformation to the block using the key."""
    for i in range(0, 4):
        for j in range(0, 4):
            block[i][j] ^= key[i][j]

def key_expansion(key: list) -> list:
    """Expand the key to be used in encryption."""
    expanded_key = to_matrix(key)  # 4x4 matrix

    byte_len = len(expanded_key)
    num_rounds = {4: 10, 6: 12, 8: 14}[byte_len]

    for index in range(byte_len, 4 * (num_rounds + 1)):
        curr_key = expanded_key[index - 1]
        # occurs every 16 bits 
        if index % byte_len == 0:
            curr_key = rot_bytes(curr_key) # mix blocks
            curr_key = sub_bytes(curr_key) # convert with SCON
            curr_key[0] ^= RCON[index // byte_len] # uses RCON
        # perform XOR
        curr_key = [i^j for i, j in zip(curr_key, expanded_key[index - byte_len])]
        expanded_key.append(curr_key)

    # divides 16 bits into (num_rounds + 1) 4x4 matrix 
    return [expanded_key[index*4:(index+1)*4] for index in range(len(expanded_key)//4)]

def encrypt_block(block: list, key: list) -> list:
    """Encrypt a 16-byte block using the key."""
    block = to_matrix(block)
    block_len = len(block)
    num_rounds = {4: 10, 6: 12, 8: 14}[block_len]

    add_round(block, key[0]) # adds round key to block

    # starts at 1 because 1 round has already taken place
    for i in range(1, num_rounds):
        block = [sub_bytes(b) for b in block]
        shift_rows(block)
        mix_columns(block)
        add_round(block, key[i])

    block = [sub_bytes(b) for b in block]
    shift_rows(block)
    add_round(block, key[-1])

    return to_bytes(block)

def encrypt(text: str, key: str):
    """Encrypt the given text using the key."""
    text_bytes = text.encode('utf-8')
    key_bytes = key.encode('utf-8')

    padded_text = pkcs7_padding(text_bytes, 16)
    expanded_key = key_expansion(list(key_bytes))

    # Each 16 bytes (128 bits) form a block in the encrypted text
    encrypted_bytes = encrypt_block(padded_text, expanded_key)

    # encrypted_bytes = bytes(encrypted_blocks) # to bytes list
    encrypted_base64 = base64.b64encode(encrypted_bytes) # to base64
    encrypted_text = encrypted_base64.decode('utf-8')

    return encrypted_text

def decrypt_block(block: list, key: list) -> list:
    """Decrypt a 16-byte block using the key."""
    block = to_matrix(block)
    num_rounds = len(key) - 1

    add_round(block, key[-1]) # opperates on the last character now

    shift_rows_inverse(block)
    block = [sub_bytes_inv(b) for b in block]

    # decryption works backwards
    for i in range(num_rounds - 1, 0, -1):
        add_round(block, key[i])
        mix_columns_inverse(block)
        shift_rows_inverse(block)
        block = [sub_bytes_inv(b) for b in block]
    
    add_round(block, key[0])

    return to_bytes(block)

def decrypt(text: str, key: str):
    """Decrypt the given encrypted text using the key."""
    text_bytes = base64.b64decode(text)  # Decode base64 before decryption
    key_bytes = key.encode('utf-8')

    padded_key = pkcs7_padding(key_bytes, 16)
    expanded_key = key_expansion(list(padded_key))

    # Each 16 bytes (128 bits) form a block in the encrypted text
    decrypted_bytes = decrypt_block(text_bytes, expanded_key)

    # Remove padding based on the last byte
    padding_length = decrypted_bytes[-1]
    decrypted_text = decrypted_bytes[:-padding_length].decode('utf-8')

    return decrypted_text

## TEST ##
# information
key = "8k6L5zkwStZxVGzX" # Set the key to your desired key (e.g., '8k6L5zkwStZxVGzX')
text = "hello world" # Set the text to whatever you want

# process
encrypted_text = encrypt(text, key)
# decrypted_text = decrypt(encrypted_text, key)

# output
print("### AES TEST ###")
print(f"Information\n\tKey:\t{key}\n\tText:\t{text}")
print(f"Encrypted:\t{encrypted_text}")
# print(f"Decrypted:\t{decrypted_text}")
print(f"Decrypted:\tNA")