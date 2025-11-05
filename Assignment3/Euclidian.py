def euclidean_gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def extended_euclidean(a, b):
    old_r, r = a, b
    old_s, s = 1, 0    # old_s*says “how much a” makes old_r
    old_t, t = 0, 1    # old_t*says “how much b” makes old_r

    while r != 0:
        quotient = old_r // r      # q = floor division
        # remainder update (Euclid):
        old_r, r = r, old_r - quotient * r
        # coefficient updates to preserve:
        # old_r == old_s*a + old_t*b (invariant)
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t  # gcd, x, y



def modular_inverse(a, m):
    gcd, x, y = extended_euclidean(a, m)
    if gcd != 1:
        return None  # inverse does not exist
    else:
        return (x % m + m) % m


def main():
    a = int(input("Enter first integer (a): "))
    b = int(input("Enter second integer (b): "))

    gcd_value = euclidean_gcd(a, b)
    print(f"GCD of {a} and {b} (Euclidean Algorithm) = {gcd_value}")

    gcd_ext, x, y = extended_euclidean(a, b)
    print("Using Extended Euclidean Algorithm:")
    print(f"GCD = {gcd_ext}, x = {x}, y = {y}")
    print(f"Verification: {a}*({x}) + {b}*({y}) = {a * x + b * y}")

    if gcd_ext == 1:
        inverse = modular_inverse(a, b)
        print(f"Modular Inverse of {a} mod {b} = {inverse}")
    else:
        print("Modular Inverse does not exist since GCD != 1")


if __name__ == "__main__":
    main()
