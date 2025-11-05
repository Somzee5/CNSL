import numpy as np

# ----------- a. Caesar Cipher ------------
 
def caesar_encrypt(plaintext, shift):
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            ciphertext += chr((ord(char) - offset + shift) % 26 + offset)
        else:
            ciphertext += char
    return ciphertext

def caesar_decrypt(ciphertext, shift):
    return caesar_encrypt(ciphertext, -shift)


# ----------- b. Playfair Cipher ------------

def playfair_prepare_text(text):
    text = text.upper().replace('J', 'I')
    prepared = ""
    i = 0
    while i < len(text):
        char1 = text[i]
        if i + 1 < len(text):
            char2 = text[i+1]
            if char1 == char2:
                prepared += char1 + 'X'
                i += 1
            else:
                prepared += char1 + char2
                i += 2
        else:
            prepared += char1 + 'X'
            i += 1
    return prepared

def playfair_generate_key_matrix(key):
    key = key.upper().replace('J', 'I')
    matrix = []
    used = set()
    for char in key:
        if char not in used and char.isalpha():
            matrix.append(char)
            used.add(char)
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in used:
            matrix.append(char)
            used.add(char)
    return np.array(matrix).reshape(5,5)

def playfair_find_pos(matrix, char):
    pos = np.where(matrix == char)
    return pos[0][0], pos[1][0]

def playfair_encrypt(plaintext, key):
    matrix = playfair_generate_key_matrix(key)
    prepared_text = playfair_prepare_text(plaintext)
    ciphertext = ""
    for i in range(0, len(prepared_text), 2):
        a, b = prepared_text[i], prepared_text[i+1]
        r1, c1 = playfair_find_pos(matrix, a)
        r2, c2 = playfair_find_pos(matrix, b)
        if r1 == r2:
            ciphertext += matrix[r1, (c1+1) % 5] + matrix[r2, (c2+1) % 5]
        elif c1 == c2:
            ciphertext += matrix[(r1+1) % 5, c1] + matrix[(r2+1) % 5, c2]
        else:
            ciphertext += matrix[r1, c2] + matrix[r2, c1]
    return ciphertext

def playfair_decrypt(ciphertext, key):
    matrix = playfair_generate_key_matrix(key)
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i+1]
        r1, c1 = playfair_find_pos(matrix, a)
        r2, c2 = playfair_find_pos(matrix, b)
        if r1 == r2:
            plaintext += matrix[r1, (c1-1) % 5] + matrix[r2, (c2-1) % 5]
        elif c1 == c2:
            plaintext += matrix[(r1-1) % 5, c1] + matrix[(r2-1) % 5, c2]
        else:
            plaintext += matrix[r1, c2] + matrix[r2, c1]
    return plaintext


# ----------- c. Hill Cipher ------------

def hill_encrypt(plaintext, key_matrix):
    n = key_matrix.shape[0]
    # Prepare text: remove spaces and convert to uppercase
    plaintext = plaintext.upper().replace(" ", "")
    # Pad plaintext if not multiple of n
    while len(plaintext) % n != 0:
        plaintext += 'X'
    ciphertext = ""
    for i in range(0, len(plaintext), n):
        block = plaintext[i:i+n]
        vector = [ord(char) - 65 for char in block]
        encrypted_vector = np.dot(key_matrix, vector) % 26
        ciphertext += "".join(chr(num + 65) for num in encrypted_vector)
    return ciphertext

def hill_decrypt(ciphertext, key_matrix):
    n = key_matrix.shape[0]
    # Find inverse of key matrix mod 26
    det = int(round(np.linalg.det(key_matrix)))  # determinant
    det_inv = None
    for i in range(26):
        if (det * i) % 26 == 1:
            det_inv = i
            break
    if det_inv is None:
        raise ValueError("Matrix not invertible modulo 26")
    # Matrix of cofactors
    cofactors = np.linalg.inv(key_matrix).T * det
    adjugate = np.round(cofactors).astype(int) % 26
    inv_key = (det_inv * adjugate) % 26

    plaintext = ""
    for i in range(0, len(ciphertext), n):
        block = ciphertext[i:i+n]
        vector = [ord(char) - 65 for char in block]
        decrypted_vector = np.dot(inv_key, vector) % 26
        plaintext += "".join(chr(int(round(num)) + 65) for num in decrypted_vector)
    return plaintext


# ----------- d. Vigenere Cipher ------------

def vigenere_encrypt(plaintext, key):
    ciphertext = ""
    key = key.upper()
    key_length = len(key)
    for i, char in enumerate(plaintext):
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            key_char = key[i % key_length]
            key_val = ord(key_char) - 65
            ciphertext += chr((ord(char) - offset + key_val) % 26 + offset)
        else:
            ciphertext += char
    return ciphertext

def vigenere_decrypt(ciphertext, key):
    plaintext = ""
    key = key.upper()
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            key_char = key[i % key_length]
            key_val = ord(key_char) - 65
            plaintext += chr((ord(char) - offset - key_val) % 26 + offset)
        else:
            plaintext += char
    return plaintext


# ----------- Testing all ciphers ------------
def test_all():
    print("----- Caesar Cipher -----")
    text = input("Enter plaintext for Caesar cipher: ")
    shift = int(input("Enter shift value (e.g., 3): "))
    encrypted = caesar_encrypt(text, shift)
    print(f"Encrypted: {encrypted}")
    decrypted = caesar_decrypt(encrypted, shift)
    print(f"Decrypted: {decrypted}\n")

    print("----- Playfair Cipher -----")
    text = input("Enter plaintext for Playfair cipher: ")
    key = input("Enter key (e.g., MONARCHY): ")
    encrypted = playfair_encrypt(text, key)
    print(f"Encrypted: {encrypted}")
    decrypted = playfair_decrypt(encrypted, key)
    print(f"Decrypted: {decrypted}\n")

    print("----- Hill Cipher -----")
    try:
        text = input("Enter plaintext for Hill cipher (even length, e.g., HELP): ")
        key_str = input("Enter key matrix values (e.g., '3 3 2 5' for [[3, 3], [2, 5]]): ")
        key_values = list(map(int, key_str.split()))
        key_matrix = np.array(key_values).reshape(2, 2)
        encrypted = hill_encrypt(text, key_matrix)
        print(f"Encrypted: {encrypted}")
        decrypted = hill_decrypt(encrypted, key_matrix)
        print(f"Decrypted: {decrypted}\n")
    except ValueError as e:
        print(f"Error: {e}\n")

    print("----- Vigenere Cipher -----")
    text = input("Enter plaintext for Vigenere cipher: ")
    key = input("Enter key (e.g., KEY): ")
    encrypted = vigenere_encrypt(text, key)
    print(f"Encrypted: {encrypted}")
    decrypted = vigenere_decrypt(encrypted, key)
    print(f"Decrypted: {decrypted}\n")

# Run the test function
if __name__ == "__main__":
    test_all()

# def test_all():
#     print("----- Caesar Cipher -----")
#     text = "HELLO WORLD"
#     shift = 3
#     encrypted = caesar_encrypt(text, shift)
#     print("Encrypted:", encrypted)
#     decrypted = caesar_decrypt(encrypted, shift)
#     print("Decrypted:", decrypted)
#     print()

#     print("----- Playfair Cipher -----")
#     text = "HELLO"
#     key = "MONARCHY"
#     encrypted = playfair_encrypt(text, key)
#     print("Encrypted:", encrypted)
#     decrypted = playfair_decrypt(encrypted, key)
#     print("Decrypted:", decrypted)
#     print()

#     print("----- Hill Cipher -----")
#     text = "HELP"
#     key_matrix = np.array([[3, 3], [2, 5]])
#     encrypted = hill_encrypt(text, key_matrix)
#     print("Encrypted:", encrypted)
#     decrypted = hill_decrypt(encrypted, key_matrix)
#     print("Decrypted:", decrypted)
#     print()

#     print("----- Vigenere Cipher -----")
#     text = "HELLO WORLD"
#     key = "KEY"
#     encrypted = vigenere_encrypt(text, key)
#     print("Encrypted:", encrypted)
#     decrypted = vigenere_decrypt(encrypted, key)
#     print("Decrypted:", decrypted)


# if __name__ == "__main__":
#     test_all()


