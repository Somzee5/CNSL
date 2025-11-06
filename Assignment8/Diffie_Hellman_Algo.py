import secrets
import time

def pow_mod(base, exp, mod):
    # Square-and-multiply modular exponentiation
    result = 1
    b = base % mod
    e = exp
    while e > 0:
        if e & 1:
            result = (result * b) % mod
        b = (b * b) % mod
        e >>= 1
    return result

def dh_keypair(p: int, g: int, priv_bits: int = None):
    # If priv_bits is None, choose exponent uniformly in [2, p-2]
    if priv_bits is None:
        # sample in [2, p-2]
        a = 2 + secrets.randbelow(p - 3)
    else:
        # sample a fixed-size secret, then reduce to [2, p-2]
        a = 2 + (int.from_bytes(secrets.token_bytes((priv_bits + 7)//8), 'big') % (p - 3))
    A = pow_mod(g, a, p)
    return a, A

def dh_shared(pub_other: int, priv: int, p: int):
    return pow_mod(pub_other, priv, p)

def demo_small():
    print("=== DH small example (didactic) ===")
    p = 23
    g = 5
    print(f"Public parameters: p={p}, g={g}")
    a, A = dh_keypair(p, g)
    b, B = dh_keypair(p, g)
    print(f"Alice: a={a}, A=g^a mod p={A}")
    print(f"Bob:   b={b}, B=g^b mod p={B}")
    K_alice = dh_shared(B, a, p)
    K_bob   = dh_shared(A, b, p)
    print(f"K_alice = B^a mod p = {K_alice}")
    print(f"K_bob   = A^b mod p = {K_bob}")
    print("Keys equal:", K_alice == K_bob)

def demo_ffdhe2048():
    print("\n=== DH large example (ffdhe2048 parameters) ===")
    # RFC 7919 Group 14 (ffdhe2048): g=2, p is a specific 2048-bit safe prime
    g = 2
    p_hex = (
        "FFFFFFFFFFFFFFFFADF85458A2BB4A9AAFDC5620273D3CF1"
        "D8B9C583CE2D3695A9E13641146433FBCC939DCE249B3EF9"
        "7D2FE363630C75D8F681B202AEC4617AD3DF1ED5D5FD6561"
        "2433F51F5F066ED0856365553DED1AF3B557135E7F57C935"
        "984F0C70E0E68B77E2A689DAF3EFE8721DF158A136ADE735"
        "30ACCA4F483A797ABC0AB182B324FB61D108A94BB2C8E3FB"
        "B96ADAB760D7F4681D4F42A3DE394DF4AE56EDE76372BB19"
        "0B07A7C8EE0A6D709E02FCE1CDF7E2ECC03404CD28342F61"
        "9172FE9CE98583FF8E4F1232EEF28183C3FE3B1B4C6FAD73"
        "3BB5FCBC2EC22005C58EF1837D1683B2C6F34A26C1B2EFFA"
        "886B423861285C97FFFFFFFFFFFFFFFF"
    )
    p = int(p_hex, 16)
    print(f"Public parameters: p bits={p.bit_length()}, g={g}")

    # Per RFC 7919 guidance, use at least 225-bit exponents for ffdhe2048
    t0 = time.time()
    a, A = dh_keypair(p, g, priv_bits=256)
    b, B = dh_keypair(p, g, priv_bits=256)
    t1 = time.time()
    print(f"Alice A=g^a mod p: {A.bit_length()} bits")
    print(f"Bob   B=g^b mod p: {B.bit_length()} bits")
    print(f"Keypair generation time: {t1 - t0:.4f} s")

    t2 = time.time()
    K_alice = dh_shared(B, a, p)
    K_bob   = dh_shared(A, b, p)
    t3 = time.time()
    print(f"Shared key bits: {K_alice.bit_length()}")
    print(f"Key agreement time: {t3 - t2:.4f} s")
    print("Keys equal:", K_alice == K_bob)

    # Derive a symmetric key from K via a KDF in real systems; here we just show hex truncation
    k_bytes = K_alice.to_bytes((K_alice.bit_length()+7)//8, 'big')
    print("Example derived key (SHA-256 placeholder not applied):", k_bytes[:16].hex(), "...")

def simulate_eavesdropper():
    print("\n=== Eavesdropper simulation (public transcript only) ===")
    p = 23
    g = 5
    a, A = dh_keypair(p, g)
    b, B = dh_keypair(p, g)
    print(f"Public transcript: p={p}, g={g}, A={A}, B={B}")
    print("Eve sees only (p,g,A,B) and must solve discrete logs to recover a or b,")
    print("which is infeasible for large parameters due to DLP hardness.")
    # For small demo parameters, Eve could brute force a by checking g^x == A mod p.

if __name__ == "__main__":
    demo_small()
    demo_ffdhe2048()
    simulate_eavesdropper()
