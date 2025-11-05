from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes 
from cryptography.hazmat.backends import default_backend 
from cryptography.hazmat.primitives import padding 
import os 
 
# Generate key and IV 
key = os.urandom(32)  # 256-bit key 
iv = os.urandom(16)   # 128-bit IV 
 
# AES cipher 
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend()) 
 
# Pad plaintext to block size (16 bytes) 
padder = padding.PKCS7(128).padder()  # 128 bits = 16 bytes block 
plaintext = b"Lets take AES Demo" 
padded_data = padder.update(plaintext) + padder.finalize() 
 
# Encrypt 
encryptor = cipher.encryptor() 
ciphertext = encryptor.update(padded_data) + encryptor.finalize() 
print("Ciphertext:", ciphertext) 
 
# Decrypt 
decryptor = cipher.decryptor() 
decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize() 
 
# Remove padding 
unpadder = padding.PKCS7(128).unpadder() 
decrypted = unpadder.update(decrypted_padded) + unpadder.finalize() 
print("Decrypted:", decrypted.decode())