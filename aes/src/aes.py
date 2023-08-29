from aes.src.utils import *

## AES ##
class AES:
    def __init__(self, key: str) -> None:
        assert len(key) in [16, 24, 32], "Invalid key length. AES allows 16, 24, or 32 key lengths."
        self.key = key # global key
        self.rounds = {4: 10, 6: 12, 8: 14}[len(key) // 4]  # rounds based on key length
        self.expanded_key = self.key_schedule(key) # expanded key

        self.default_iv = b"\x01" * 16 # used when cbc is checked but not iv provided

    @record_time
    def key_schedule(self, key: str) -> list:
        """Expand the key to be used in encryption."""
        expanded_key = to_matrix(list(key.encode("utf-8")))  # 4x4 matrix
        iteration_size = len(key) // 4 # Number of words in the key (4 bytes per word)

        # Loop to generate round keys
        for index in range(len(expanded_key), 4 * (self.rounds + 1)):
            current_word_block = expanded_key[-1] # 1 word block (last of list)
            
            if len(expanded_key) % iteration_size == 0:
                current_word_block = self.sub_bytes(self.rot_bytes(current_word_block)) # Apply Rot & Sub
                current_word_block[0] ^= RCON[index // iteration_size] # Apply RCON

            elif len(self.key) == 32 and len(expanded_key) % iteration_size == 4: # Special case for 256-bit key
                current_word_block = self.sub_bytes(current_word_block)

            # XOR the current word block with the word block at (current - iteration_size) position
            current_word_block = xor(current_word_block, expanded_key[-iteration_size]) # XOR
            expanded_key.append(current_word_block) # Add generated word block to expanded key

        return expanded_key # 44 word_blocks => 11 keys

    def encrypt_block(self, text: bytes) -> bytes:
        """Encrypt a 16 byte block using standard AES."""
        plaintext = pkcs7_padding(text) # Encodes and adds padding
        word_block_matrix = to_matrix(plaintext) # Convert the padded text to a (decimal) matrix

        # Initial round (just add_round)
        self.add_round(word_block_matrix, self.expanded_key[:4])

        # Main encryption loop
        for index in range(1, self.rounds):
            word_block_matrix = [self.sub_bytes(wb) for wb in word_block_matrix] # Sub bytes
            self.shift_rows(word_block_matrix) # Shift rows
            self.mix_columns(word_block_matrix) # Mix columns
            self.add_round(word_block_matrix, self.expanded_key[4 * index: 4 * (index + 1)]) # Add round

        # Final round (all but mix_columns)
        word_block_matrix = [self.sub_bytes(wb) for wb in word_block_matrix]
        self.shift_rows(word_block_matrix)
        self.add_round(word_block_matrix, self.expanded_key[-4:])

        # Convert (decimal) matrix back to bytes
        return to_bytes(word_block_matrix)

    def decrypt_block(self, text: bytes) -> bytes:
        """Decrypt a 16 byte block using standard AES."""
        word_block_matrix = to_matrix(text) # Converts bytes to a (deciaml) matrix

        # Initial round (all but mix_columns)
        self.add_round(word_block_matrix, self.expanded_key[-4:])
        self.shift_rows(word_block_matrix, inverse=True)
        word_block_matrix = [self.sub_bytes(wb, inverse=True) for wb in word_block_matrix]

        # Main decryption loop
        for index in range(self.rounds - 1, 0, -1):
            self.add_round(word_block_matrix, self.expanded_key[4 * index: 4 * (index + 1)]) # Add round
            self.mix_columns(word_block_matrix, inverse=True) # Inverse mix columns
            self.shift_rows(word_block_matrix, inverse=True) # Inverse shift rows
            word_block_matrix = [self.sub_bytes(wb, inverse=True) for wb in word_block_matrix] # Inverse sub bytes

        # Final round (just add_round)
        self.add_round(word_block_matrix, self.expanded_key[:4])

        plaintext = to_bytes(word_block_matrix)
        original_text = pkcs7_padding_undo(plaintext)

        return original_text

    @record_time
    def encrypt(self, text: str, cbc=False, iv=None) -> bytes:
        """Encrypt the given text using the key. CBC is an option that uses an IV to add an extra layer of security."""
        encoded_text = text.encode("utf-8")

        chunks = load_chunks(encoded_text) # split incoming text into chunks of 16 bytes
        encrypted_text = bytes() # variable for encrypted blocks to be added

        # check to see if cbc is being used and fetch an iv
        previous = (iv.encode("utf-8") if iv is not None else self.default_iv) if cbc else None # iv used for cbc 

        # main encryption loop
        for chunk in chunks:
            if not cbc: 
                encrypted_text += self.encrypt_block(chunk)
            else:
                new_chunk = self.encrypt_block(xor(chunk, previous)) # encrypt chunk
                previous = new_chunk # sets new previous
                encrypted_text += new_chunk # adds new chunk
        
        return encrypted_text
                
    @record_time
    def decrypt(self, text: bytes, cbc=False, iv=None) -> str:
        """Decrypt the given bytes using the key. CBC is an option that uses an IV to add an extra layer of security."""
        chunks = load_chunks(text) # split incoming text into chunks of 16 bytes
        decrypted_text = bytes() # variable for decrypted blocks to be added

        # check to see if cbc is being used and fetch an iv
        previous = (iv.encode("utf-8") if iv is not None else self.default_iv) if cbc else None # iv used for cbc 

        # main decryption loop
        for chunk in chunks:
            if not cbc: 
                decrypted_text += self.decrypt_block(chunk)
            else:
                decrypted_text += xor(previous, self.decrypt_block(chunk)) # adds new chunk
                previous = chunk # sets new previous

        return decrypted_text.decode("utf-8")

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