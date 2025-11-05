from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# For CTR with 3DES, a 64-bit (8-byte) nonce/counter block is typical.
# cryptography's CTR takes an initial counter block (bytes).

def encrypt_3DES_CTR(key_24b: bytes, plaintext: bytes):
    nonce = os.urandom(8)  # 8 bytes for DES block size
    cipher = Cipher(algorithms.TripleDES(key_24b), modes.CTR(nonce), backend=default_backend())
    enc = cipher.encryptor().update(plaintext) + cipher.encryptor().finalize()
    return nonce + enc

def decrypt_3DES_CTR(key_24b: bytes, data: bytes):
    nonce, ct = data[:8], data[8:]
    cipher = Cipher(algorithms.TripleDES(key_24b), modes.CTR(nonce), backend=default_backend())
    pt = cipher.decryptor().update(ct) + cipher.decryptor().finalize()
    return pt

# Example usage:
key = b"12345678abcdefgh12345678"
msg = b"SalaryInfo2025"
blob = encrypt_3DES_CTR(key, msg)
plain = decrypt_3DES_CTR(key, blob)
print("CTR hex:", blob.hex().upper())
print("CTR dec:", plain.decode())
