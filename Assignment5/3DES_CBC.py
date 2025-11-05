# 3DES-CBC with PKCS7 padding (8-byte IV)

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

BLOCK_SIZE_BYTES = 8  # DES/3DES block size

def encrypt_3DES_CBC(key_24b: bytes, plaintext: bytes):
    # PKCS7 pad to 8-byte blocks
    padder = padding.PKCS7(BLOCK_SIZE_BYTES * 8).padder()
    padded = padder.update(plaintext) + padder.finalize()

    iv = os.urandom(BLOCK_SIZE_BYTES)  # 8-byte IV for 3DES
    cipher = Cipher(algorithms.TripleDES(key_24b), modes.CBC(iv), backend=default_backend())
    enc = cipher.encryptor().update(padded) + cipher.encryptor().finalize()
    return iv + enc  # prepend IV for transport

def decrypt_3DES_CBC(key_24b: bytes, data: bytes):
    iv, ct = data[:BLOCK_SIZE_BYTES], data[BLOCK_SIZE_BYTES:]
    cipher = Cipher(algorithms.TripleDES(key_24b), modes.CBC(iv), backend=default_backend())
    padded = cipher.decryptor().update(ct) + cipher.decryptor().finalize()

    unpadder = padding.PKCS7(BLOCK_SIZE_BYTES * 8).unpadder()
    pt = unpadder.update(padded) + unpadder.finalize()
    return pt

# Example usage:
key = b"12345678abcdefgh12345678"  # 24 bytes
msg = b"ConfidentialMsg"
blob = encrypt_3DES_CBC(key, msg)
plain = decrypt_3DES_CBC(key, blob)
print("CBC hex:", blob.hex().upper())
print("CBC dec:", plain.decode())
