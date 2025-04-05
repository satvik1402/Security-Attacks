import random
from math import gcd

# Compute Jacobi symbol (a/n)
def jacobi(a, n):
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be a positive odd number.")
    
    a = a % n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a = a // 2
            if n % 8 in [3, 5]:
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a = a % n
    return result if n == 1 else 0

# Solovay-Strassen Primality Test
def is_probably_prime(n, k=5):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for _ in range(k):
        a = random.randrange(2, n - 1)
        if gcd(a, n) > 1:
            return False
        jac = jacobi(a, n) % n
        mod_exp = pow(a, (n - 1) // 2, n)
        if jac != mod_exp:
            return False
    return True

# --- Example Usage ---

candidates = [7, 13, 15, 17, 21, 23, 561, 1105, 1729]  # includes Carmichael numbers
print("Solovay-Strassen Primality Test Results:\n")
for n in candidates:
    result = is_probably_prime(n, k=10)
    print(f"{n}: {'Probably Prime' if result else 'Composite'}")