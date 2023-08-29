import time

## UTILS ##
def to_matrix(block: list) -> list:
    """Convert a 16-byte block to a 4x4 matrix."""
    return [list(block[index:index+4]) for index in range(0, len(block), 4)]

def to_bytes(block: list) -> bytes:
    """Convert a 4x4 matrix to a 16-byte block."""
    return bytes(sum(block, []))

def pkcs7_padding(data: bytes) -> bytes:
    """Apply PKCS#7 padding to the data to make it a multiple of 16."""
    padding_length = (16 - len(data)) % 16 # adds padding up to a len of 16
    padding = bytes([padding_length] * padding_length)
    return data + padding

def pkcs7_padding_undo(data: bytes):
    """Removes application of PKCS#7 padding."""
    return data[:-data[-1]] if data[-1] in range(1, 16) else data 

def galois(a, b):
    """Implementation of Galois field."""
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        carry = a & 0x80
        a <<= 1
        if carry:
            a ^= 0x1B  # xtime(0x80) in the Galois field (0x1B)
        b >>= 1
    return p % 256

def xor(a, b) -> bytes:
    return bytes(i ^ j for i, j in zip(a, b))

def load_chunks(input) -> list:
    """Creates blocks of data in chunks of 16 characters of bytes."""
    chunks = []
    for index in range(0, len(input), 16):
        chunks.append(input[index: index + 16])
    return chunks

def record_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"* {func.__name__}:\t{execution_time:.6f} seconds")
        return result
    return wrapper