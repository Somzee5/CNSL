def create_order(key):
    """
    Creates the permutation order based on the alphabetical order of the key.
    For example, if key is "ZEBRAS", the sorted key is "ABERSZ".
    The order would be:
    Z (6th in sorted) -> 6
    E (2nd in sorted) -> 2
    B (1st in sorted) -> 1
    R (4th in sorted) -> 4
    A (0th in sorted) -> 0
    S (5th in sorted) -> 5
    """
    sorted_key = sorted(key)
    order = []
    for k_char in key:
        # Find the index of the character in the sorted key and add 1
        # to make it 1-based as in the C++ code.
        order.append(sorted_key.index(k_char) + 1)
        # To handle duplicate characters in the key (if allowed, though not common for transposition)
        # one might need to remove the character from sorted_key after finding it.
        # However, for typical transposition keys, characters are unique.
    return order

def row_column_encrypt(plaintext, key):
    """
    Encrypts a plaintext using the row-column transposition cipher.
    """
    key_len = len(key)
    order = create_order(key)

    # Remove spaces from plaintext and convert to uppercase for consistency
    plaintext = plaintext.replace(" ", "").upper()

    # Calculate the number of rows needed
    rows = (len(plaintext) + key_len - 1) // key_len  # Equivalent to ceil(len(plaintext) / key_len)

    # Create the matrix, padding with 'X'
    matrix = [['X'] * key_len for _ in range(rows)]

    index = 0
    for r in range(rows):
        for c in range(key_len):
            if index < len(plaintext):
                matrix[r][c] = plaintext[index]
                index += 1

    ciphertext = []
    # Read the columns in the order defined by the key
    for num in range(1, key_len + 1):
        # Find the original column index corresponding to the current order number
        col = order.index(num)
        for r in range(rows):
            ciphertext.append(matrix[r][col])

    return "".join(ciphertext)

def row_column_decrypt(ciphertext, key):
    """
    Decrypts a ciphertext encrypted with the row-column transposition cipher.
    """
    key_len = len(key)
    order = create_order(key)

    # Calculate the number of rows (ciphertext length must be a multiple of key_len)
    rows = len(ciphertext) // key_len

    # Create an empty matrix to fill
    matrix = [['\0'] * key_len for _ in range(rows)]

    index = 0
    # Fill the matrix by reading columns in the order defined by the key
    for num in range(1, key_len + 1):
        col = order.index(num)
        for r in range(rows):
            matrix[r][col] = ciphertext[index]
            index += 1

    plaintext = []
    # Read the matrix row by row to reconstruct the plaintext
    for r in range(rows):
        for c in range(key_len):
            plaintext.append(matrix[r][c])

    # Remove padding 'X' characters from the end
    while plaintext and plaintext[-1] == 'X':
        plaintext.pop()

    return "".join(plaintext)

if __name__ == "__main__":
    key = "ZEBRAS"
    plaintext = "WE ARE DISCOVERED RUN AT ONCE"

    encrypted = row_column_encrypt(plaintext, key)
    print("Encrypted:", encrypted)

    decrypted = row_column_decrypt(encrypted, key)
    print("Decrypted:", decrypted)