import math 
import secrets 
import time 
 
def is_prime(n, k=40): 
    if n < 2: 
        return False 
    if n % 2 == 0: 
        return n == 2 
    r, s = 0, n - 1 
    while s % 2 == 0: 
        r += 1 
        s //= 2 
    for _ in range(k): 
        a = secrets.randbelow(n - 3) + 2 
        x = pow(a, s, n) 
        if x == 1 or x == n - 1: 
            continue 
        for _ in range(r - 1): 
            x = pow(x, 2, n) 
            if x == n - 1: 
                break 
        else: 
            return False 
    return True 
 
def generate_large_prime(bits): 
    while True: 
        candidate = secrets.randbits(bits) 
        candidate |= (1 << bits - 1) | 1 
        if is_prime(candidate): 
            return candidate 
 
def egcd(a, b): 
    if a == 0: 
        return b, 0, 1 
    g, y, x = egcd(b % a, a) 
    return g, x - (b // a) * y, y 
def modinv(a, m): 
    g, x, y = egcd(a, m) 
    if g != 1: 
        raise Exception('modular inverse does not exist') 
    return x % m 
 
def generate_keypair(bits=1024): 
    p = generate_large_prime(bits // 2) 
    q = generate_large_prime(bits // 2) 
    n = p * q 
    phi = (p - 1) * (q - 1) 
    e = 65537 
    if math.gcd(e, phi) != 1: 
        e = 3 
        while math.gcd(e, phi) != 1: 
            e += 2 
    d = modinv(e, phi) 
    public_key = (n, e) 
    private_key = (n, d) 
    return public_key, private_key, (p, q) 
 
def encrypt(public_key, plaintext_bytes): 
    n, e = public_key 
    m = int.from_bytes(plaintext_bytes, byteorder='big') 
    if m >= n: 
        raise ValueError('message too large for the key size') 
    c = pow(m, e, n) 
    return c 
 
def decrypt(private_key, ciphertext_int): 
    n, d = private_key 
    m = pow(ciphertext_int, d, n) 
    byte_length = (m.bit_length() + 7) // 8 
    return m.to_bytes(byte_length, byteorder='big') 
 
if __name__ == '__main__': 
    message = b"Hello RSA! This is a short test." 
    print('Message:', message) 
 
    for bits in (1024, 2048): 
        print('\n--- Testing with', bits, 'bit keys ---') 
        t0 = time.time() 
        pub, priv, primes = generate_keypair(bits) 
        t1 = time.time() 
        print('Key generation time: {:.2f}s'.format(t1 - t0)) 
        n, e = pub 
        print('n bit-length:', n.bit_length()) 
 
        t0 = time.time() 
        ciphertext = encrypt(pub, message) 
        t1 = time.time() 
        print('Encrypt time: {:.4f}s'.format(t1 - t0)) 
 
 
 
        t0 = time.time() 
        plaintext = decrypt(priv, ciphertext) 
        t1 = time.time() 
        print('Decrypt time: {:.4f}s'.format(t1 - t0)) 
 
        print('Decrypted equals original?', plaintext == message) 