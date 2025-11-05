def rail_fence_encrypt(text, key):

    rail = [['\n' for i in range(len(text))] for j in range(key)]

    dir_down = False

    row, col = 0, 0

    for char in text:

        if row == 0 or row == key - 1:

            dir_down = not dir_down

        rail[row][col] = char

        col += 1

        row += 1 if dir_down else -1

    result = []

    for i in range(key):

        for j in range(len(text)):

            if rail[i][j] != '\n':

                result.append(rail[i][j])

    return "".join(result)

def rail_fence_decrypt(cipher, key):

    rail = [['\n' for i in range(len(cipher))] for j in range(key)]

    dir_down = None

    row, col = 0, 0

    for i in range(len(cipher)):

        if row == 0:

            dir_down = True

        if row == key - 1:

            dir_down = False

        rail[row][col] = '*'

        col += 1

        row += 1 if dir_down else -1

    index = 0

    for i in range(key):

        for j in range(len(cipher)):

            if rail[i][j] == '*' and index < len(cipher):

                rail[i][j] = cipher[index]

                index += 1

    result = []

    row, col = 0, 0

    for i in range(len(cipher)):

        if row == 0:

            dir_down = True

        if row == key - 1:

            dir_down = False

        if rail[row][col] != '*':

            result.append(rail[row][col])

            col += 1

        row += 1 if dir_down else -1

    return "".join(result)

# Example:

plaintext = "HELLOWORLD"

key = 3

ciphertext = rail_fence_encrypt(plaintext, key)

print("Encrypted:", ciphertext)

decrypted = rail_fence_decrypt(ciphertext, key)

print("Decrypted:", decrypted)

