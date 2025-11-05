from math import gcd 
from functools import reduce 
 
def egcd(a, b): 
    if b == 0: 
        return (a, 1, 0) 
    g, x1, y1 = egcd(b, a % b) 
    return (g, y1, x1 - (a // b) * y1) 
 
def modinv(a, m): 
    g, x, _ = egcd(a, m) 
    if g != 1: 
        raise ValueError("Inverse does not exist") 
    return x % m 
 
def crt_pairwise_coprime(a, n): 
    N = reduce(lambda x, y: x * y, n, 1) 
    x = 0 
    for ai, ni in zip(a, n): 
        Mi = N // ni 
        yi = modinv(Mi, ni) 
        x += ai * Mi * yi 
    return x % N, N 
 
 
 
print("Example 1:") 
print("x ≡ 2 (mod 3), x ≡ 3 (mod 4), x ≡ 1 (mod 5)") 
print("Solution:", crt_pairwise_coprime([2, 3, 1], [3, 4, 5]))   
print() 
 
print("Example 2:") 
print("x ≡ 1 (mod 2), x ≡ 2 (mod 3), x ≡ 3 (mod 5)") 
print("Solution:", crt_pairwise_coprime([1, 2, 3], [2, 3, 5]))   
print() 
 
print("Example 3:") 
print("x ≡ 2 (mod 5), x ≡ 3 (mod 7), x ≡ 2 (mod 9)") 
print("Solution:", crt_pairwise_coprime([2, 3, 2], [5, 7, 9]))   
print() 
 
print("Example 4:") 
print("x ≡ 3 (mod 4), x ≡ 4 (mod 7), x ≡ 2 (mod 9)") 
print("Solution:", crt_pairwise_coprime([3, 4, 2], [4, 7, 9]))   
print() 
 
print("Example 5:") 
print("x ≡ 1 (mod 5), x ≡ 4 (mod 11), x ≡ 6 (mod 17)") 
print("Solution:", crt_pairwise_coprime([1, 4, 6], [5, 11, 17]))   
print() 