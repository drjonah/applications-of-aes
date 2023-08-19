import base64
from aes.src.utils import *

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
            current_word_block = expanded_key[index - 1] # 1 byte
            if index % 4 == 0:
                current_word_block = self.sub_bytes(self.rot_bytes(current_word_block)) # Rot & Sub
                current_word_block[0] ^= RCON[index // 4] # RCON
            # elif self.rounds > 6 and self.rounds % 4 == 4: # 256
            #     current_word_block = self.sub_bytes(current_word_block)
            current_word_block = [i ^ j for i, j in zip(current_word_block, expanded_key[index - 4])] # XOR
            expanded_key.append(current_word_block)

        return expanded_key # 44 word_blocks => 11 keys

    @record_time
    def encrypt(self, text: str) -> bytes:
        """Encrypt the given text using the key."""
        plaintext = pkcs7_padding(text.encode("utf-8")) # encodes and adds padding
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

        return to_bytes(word_block_matrix)
    
    @record_time
    def decrypt(self, text: bytes) -> str:
        word_block_matrix = to_matrix(text) # encodes to 4x4 matrix

        self.add_round(word_block_matrix, self.expanded_key[-4:])
        self.shift_rows(word_block_matrix, inverse=True)
        word_block_matrix = [self.sub_bytes(wb, inverse=True) for wb in word_block_matrix]

        for index in range(self.rounds - 1, 0, -1):
            self.add_round(word_block_matrix, self.expanded_key[4 * index: 4 * (index + 1)])
            self.mix_columns(word_block_matrix, inverse=True)
            self.shift_rows(word_block_matrix, inverse=True)
            word_block_matrix = [self.sub_bytes(wb, inverse=True) for wb in word_block_matrix]

        self.add_round(word_block_matrix, self.expanded_key[:4])

        plaintext = to_bytes(word_block_matrix)
        original_text = pkcs7_padding_undo(plaintext).decode("utf-8")

        return original_text

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
            word_block[0][1], word_block[1][1], word_block[2][1], word_block[3][1] = word_block[3][1], word_block[0][1], word_block[1][1], word_block[2][1]
            word_block[0][2], word_block[1][2], word_block[2][2], word_block[3][2] = word_block[2][2], word_block[3][2], word_block[0][2], word_block[1][2]
            word_block[0][3], word_block[1][3], word_block[2][3], word_block[3][3] = word_block[1][3], word_block[2][3], word_block[3][3], word_block[0][3]
        else:
            word_block[0][1], word_block[1][1], word_block[2][1], word_block[3][1] = word_block[1][1], word_block[2][1], word_block[3][1], word_block[0][1]
            word_block[0][2], word_block[1][2], word_block[2][2], word_block[3][2] = word_block[2][2], word_block[3][2], word_block[0][2], word_block[1][2]
            word_block[0][3], word_block[1][3], word_block[2][3], word_block[3][3] = word_block[3][3], word_block[0][3], word_block[1][3], word_block[2][3]

    def mix_columns(self, word_block_matrix: list, inverse=False) -> None:
        """Apply mix columns transformation to the block."""
        for i in range(4):
            wb0 = word_block_matrix[i][0]
            wb1 = word_block_matrix[i][1]
            wb2 = word_block_matrix[i][2]
            wb3 = word_block_matrix[i][3]

            if inverse: # inverse galois variable b= differs than a non inverse galois
                word_block_matrix[i][0] = galois(wb0, 0xE) ^ galois(wb1, 0xB) ^ galois(wb2, 0xD) ^ galois(wb3, 0x9)
                word_block_matrix[i][1] = galois(wb1, 0xE) ^ galois(wb2, 0xB) ^ galois(wb3, 0xD) ^ galois(wb0, 0x9)
                word_block_matrix[i][2] = galois(wb2, 0xE) ^ galois(wb3, 0xB) ^ galois(wb0, 0xD) ^ galois(wb1, 0x9)
                word_block_matrix[i][3] = galois(wb3, 0xE) ^ galois(wb0, 0xB) ^ galois(wb1, 0xD) ^ galois(wb2, 0x9)
            else:
                word_block_matrix[i][0] = galois(wb0, 2) ^ galois(wb1, 3) ^ wb2 ^ wb3
                word_block_matrix[i][1] = galois(wb1, 2) ^ galois(wb2, 3) ^ wb3 ^ wb0
                word_block_matrix[i][2] = galois(wb2, 2) ^ galois(wb3, 3) ^ wb0 ^ wb1
                word_block_matrix[i][3] = galois(wb3, 2) ^ galois(wb0, 3) ^ wb1 ^ wb2

    def add_round(self, word_block_matrix: list, key: list) -> None:
        """Apply key schedule transformation to the block using the key."""
        for i in range(4):
            for j in range(4):
                word_block_matrix[i][j] ^= key[i][j]