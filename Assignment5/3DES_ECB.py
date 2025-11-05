from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes 
from cryptography.hazmat.backends import default_backend 
 
def pad(text): 
    while len(text) % 8 != 0: 
        text += ' ' 
    return text 
 
def encrypt_3DES(key, plaintext): 
    plaintext = pad(plaintext).encode('utf-8') 
    cipher = Cipher(algorithms.TripleDES(key.encode('utf-8')), modes.ECB(), 
backend=default_backend()) 
    encryptor = cipher.encryptor() 
    ciphertext = encryptor.update(plaintext) + encryptor.finalize() 
    return ciphertext.hex().upper() 
 
def decrypt_3DES(key, ciphertext_hex): 
    ciphertext = bytes.fromhex(ciphertext_hex) 
    cipher = Cipher(algorithms.TripleDES(key.encode('utf-8')), modes.ECB(), 
backend=default_backend()) 
    decryptor = cipher.decryptor() 
    decrypted = decryptor.update(ciphertext) + decryptor.finalize() 
    return decrypted.decode('utf-8').rstrip() 
 
 
key = "12345678abcdefgh12345678"  # 24 bytes for TripleDES 
 
texts = ["HelloWorld", "DES Algorithm", "SecureData123", "ConfidentialMsg", 
"SalaryInfo2025"] 
 
for text in texts: 
    enc = encrypt_3DES(key, text) 
    dec = decrypt_3DES(key, enc) 
    print("Plaintext:", text) 
    print("Encrypted:", enc) 
    print("Decrypted:", dec) 
    print()