import base64
from rijndael import RCON, SBOX, SBOX_INV
from utils import to_matrix, to_bytes, pkcs7_padding, pkcs7_padding_undo, galois_multiply, record_time

## AES ##
class AES:
    def __init__(self, key: str) -> None:
        assert len(key) in [16, 24, 32], "Invalid key length. AES allows 16, 24, or 32 key lengths."
        self.key = key
        self.rounds = {4: 10, 6: 12, 8: 14}[len(key) // 4] 
        self.expanded_key = self.key_schedule(key)

    @record_time
    def key_schedule(self, key: str) -> list:
        """Expand the key to be used in encryption."""
        expanded_key = to_matrix(list(key.encode("utf-8")))  # 4x4 matrix

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
        plaintext = pkcs7_padding(text.encode('utf-8'), 16) # encodes and adds padding
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

    def rot_bytes(self, word_block: list) -> list:
        """Rotate the bytes in the block to the left by one position."""
        return word_block[1:] + word_block[:1]
    
    def sub_bytes(self, word_block: list) -> list:
        """Apply sub bytes transformation to the block."""
        return [SBOX[wb] for wb in word_block]

    def shift_rows(self, block: list) -> None:
        """Shift the rows in the block according to AES specifications."""
        block[1] = [block[1][1], block[1][2], block[1][3], block[1][0]] # shifts 1
        block[2] = [block[2][2], block[2][3], block[2][0], block[2][1]] # shifts 2
        block[3] = [block[3][3], block[3][0], block[3][1], block[3][2]] # shifts 3

    def mix_columns(sel, word_block_matrix: list) -> None:
        """Apply mix columns transformation to the block."""
        for i in range(4):
            s0 = word_block_matrix[i][0]
            s1 = word_block_matrix[i][1]
            s2 = word_block_matrix[i][2]
            s3 = word_block_matrix[i][3]

            word_block_matrix[i][0] = galois_multiply(s0, 2) ^ galois_multiply(s1, 3) ^ s2 ^ s3
            word_block_matrix[i][1] = galois_multiply(s1, 2) ^ galois_multiply(s2, 3) ^ s3 ^ s0
            word_block_matrix[i][2] = galois_multiply(s2, 2) ^ galois_multiply(s3, 3) ^ s0 ^ s1
            word_block_matrix[i][3] = galois_multiply(s3, 2) ^ galois_multiply(s0, 3) ^ s1 ^ s2

    def add_round(self, word_block_matrix: list, key: list) -> None:
        """Apply key schedule transformation to the block using the key."""
        for i in range(4):
            for j in range(4):
                word_block_matrix[i][j] ^= key[i][j]

    
## TESTS ##
print("### AES EXECUTION ###")

cipher128 = AES("8k6L5zkwStZxVGzX")
encyrpted = cipher128.encrypt("hello world")

# cipher192 = AES("hwRhjC5s2YtACanDktuXKxte")
# encyrpted = cipher192.encrypt("hello world")

# cipher256 = AES("w6HYstMa2dAxututGRaE2KPHdck9h9qg")
# encyrpted = cipher256.encrypt("hello world")

print("### AES TESTS ###")
print(f"Encrypted:\t{encyrpted}")