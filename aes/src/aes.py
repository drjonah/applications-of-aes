import base64
from rijndael import RCON, SBOX, SBOX_INV
from utils import to_matrix, to_bytes, pkcs7_padding, pkcs7_padding_undo, galois, record_time

## AES ##
class AES:
    def __init__(self, key: str) -> None:
        assert len(key) in [16, 24, 32], "Invalid key length. AES allows 16, 24, or 32 key lengths."
        self.key = key
        self.rounds = {4: 10, 6: 12, 8: 14}[len(key) // 4] 
        self.expanded_key = self.key_schedule(key)

        print(f"Original Key: {self.key} | len={len(self.key)}")
        print(f"Expanded Key: {self.expanded_key}")

    @record_time
    def key_schedule(self, key: str) -> list:
        """Expand the key to be used in encryption."""
        expanded_key = to_matrix(list(key.encode("utf-8")))  # 4x4 matrix
        # expanded_key = to_matrix([int(char, 16) for char in key])  # 4x4 matrix

        print(expanded_key)

        for index in range(4, 4 * (self.rounds + 1)):
            word_block = expanded_key[index - 1] # 1 byte
            if index % 4 == 0:
                word_block = self.sub_bytes(self.rot_bytes(word_block)) # Rot | SBOX
                word_block[0] ^= RCON[index // 4] # RCON
            elif self.rounds > 6 and self.rounds % 4 == 4: # 256
                word_block = self.sub_bytes(word_block)
            word_block = [i ^ j for i, j in zip(word_block, expanded_key[index - 4])] # XOR
            expanded_key.append(word_block)

        return expanded_key # 44 word_blocks => 11 keys

    @record_time
    def encrypt(self, text: str) -> str:
        """Encrypt the given text using the key."""
        plaintext = pkcs7_padding(text.encode('utf-8')) # encodes and adds padding
        word_block_matrix = to_matrix(plaintext)

        self.add_round(word_block_matrix, self.expanded_key[:4])

        for index in range(1, self.rounds):
            word_block_matrix = [self.sub_bytes(wb) for wb in word_block_matrix]
            self.shift_rows(word_block_matrix)
            self.mix_columns(word_block_matrix)
            self.add_round(word_block_matrix, self.expanded_key[4 * index: 4 * (index + 1)])

        word_block_matrix = [self.sub_bytes(wb) for wb in word_block_matrix]
        self.shift_rows(word_block_matrix)
        self.add_round(word_block_matrix, self.expanded_key[40:])

        # encrypted_bytes = bytes(encrypted_blocks) # to bytes list
        encrypted_base64 = base64.b64encode(to_bytes(word_block_matrix)) # to base64
        encrypted_text = encrypted_base64.decode('utf-8')

        return encrypted_text
    
    @record_time
    def decrypt(self, text: str) -> str:
        word_block_matrix = to_matrix(text.encode('utf-8')) # encodes to 4x4 matrix
        # print(word_block_matrix)
        # self.add_round(word_block_matrix, self.expanded_key[-4:])

    def rot_bytes(self, word_block: list) -> list:
        """Rotate the bytes in the block to the left by one position."""
        return word_block[1:] + word_block[:1]
    
    def sub_bytes(self, word_block: list, inverse=False) -> list:
        """Apply sub bytes transformation to the block."""
        if inverse:
            return [SBOX_INV[wb] for wb in word_block]
        return [SBOX[wb] for wb in word_block]

    def shift_rows(self, word_block: list, inverse=False) -> None:
        """Shift the rows in the block according to AES specifications."""
        if inverse:
            word_block[1] = [word_block[1][3], word_block[1][0], word_block[1][1], word_block[1][2]] # shifts -1
            word_block[2] = [word_block[2][2], word_block[2][3], word_block[2][0], word_block[2][1]] # shifts -2
            word_block[3] = [word_block[3][1], word_block[3][2], word_block[3][3], word_block[3][0]] # shifts -3
        else:
            word_block[1] = [word_block[1][1], word_block[1][2], word_block[1][3], word_block[1][0]] # shifts 1
            word_block[2] = [word_block[2][2], word_block[2][3], word_block[2][0], word_block[2][1]] # shifts 2
            word_block[3] = [word_block[3][3], word_block[3][0], word_block[3][1], word_block[3][2]] # shifts 3

    def mix_columns(self, word_block_matrix: list, inverse=False) -> None:
        """Apply mix columns transformation to the block."""
        for i in range(4):
            s0 = word_block_matrix[i][0]
            s1 = word_block_matrix[i][1]
            s2 = word_block_matrix[i][2]
            s3 = word_block_matrix[i][3]

            if inverse: # inverse galois variable b= differs than a non inverse galois
                word_block_matrix[i][0] = galois(s0, 0xE) ^ galois(s1, 0xB) ^ galois(s2, 0xD) ^ galois(s3, 0x9)
                word_block_matrix[i][1] = galois(s1, 0xE) ^ galois(s2, 0xB) ^ galois(s3, 0xD) ^ galois(s0, 0x9)
                word_block_matrix[i][2] = galois(s2, 0xE) ^ galois(s3, 0xB) ^ galois(s0, 0xD) ^ galois(s1, 0x9)
                word_block_matrix[i][3] = galois(s3, 0xE) ^ galois(s0, 0xB) ^ galois(s1, 0xD) ^ galois(s2, 0x9)
            else:
                word_block_matrix[i][0] = galois(s0, 2) ^ galois(s1, 3) ^ s2 ^ s3
                word_block_matrix[i][1] = galois(s1, 2) ^ galois(s2, 3) ^ s3 ^ s0
                word_block_matrix[i][2] = galois(s2, 2) ^ galois(s3, 3) ^ s0 ^ s1
                word_block_matrix[i][3] = galois(s3, 2) ^ galois(s0, 3) ^ s1 ^ s2

    def add_round(self, word_block_matrix: list, key: list) -> None:
        """Apply key schedule transformation to the block using the key."""
        for i in range(4):
            for j in range(4):
                word_block_matrix[i][j] ^= key[i][j]

    
## TESTS ##
print("### AES EXECUTION ###")

cipher128 = AES("0" * 16)
encrypted = cipher128.encrypt("hello world")
decrypted = cipher128.decrypt(encrypted)

# cipher192 = AES("hwRhjC5s2YtACanDktuXKxte")
# encrypted = cipher192.encrypt("hello world")

# cipher256 = AES("w6HYstMa2dAxututGRaE2KPHdck9h9qg")
# encrypted = cipher256.encrypt("hello world")

print("### AES TESTS ###")
print(f"Encrypted:\t{encrypted}")
print(f"Decrypted:\t{decrypted}")

## CREDITS ##
# Government docs: 
#   https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf 
# Galois implentation
#   http://blog.simulacrum.me/2019/01/aes-galois/
