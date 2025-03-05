def extended_euclidean(a, b):
    """
    Extended Euclidean Algorithm to find modular multiplicative inverse
    Returns (gcd, x, y) where gcd is the greatest common divisor and 
    x, y are coefficients such that ax + by = gcd
    """
    if a == 0:
        return b, 0, 1
    
    gcd, x1, y1 = extended_euclidean(b % a, a)
    
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd, x, y

def mod_inverse(a, m):
    """
    Find modular multiplicative inverse of a modulo m
    """
    gcd, x, _ = extended_euclidean(a, m)
    
    if gcd != 1:
        raise ValueError(f'Modular inverse does not exist for {a} mod {m}')
    
    return x % m

def chinese_remainder_theorem(remainders, moduli):
    """
    Solve system of linear congruences using Chinese Remainder Theorem
    
    Args:
    - remainders: list of remainder values [a1, a2, ..., an]
    - moduli: list of moduli [n1, n2, ..., nn]
    
    Returns:
    - Unique solution x such that x ≡ ai (mod ni) for all i
    """
    # Total modulus (product of all moduli)
    N = 1
    for m in moduli:
        N *= m
    
    # Solve the system
    x = 0
    for ai, ni in zip(remainders, moduli):
        # Calculate Ni (product of all moduli except current)
        Ni = N // ni
        
        # Find modular multiplicative inverse
        mi = mod_inverse(Ni, ni)
        
        # Add to solution
        x += ai * Ni * mi
    
    return x % N

# Specific problem solution
remainders = [2, 3, 5]
moduli = [5, 11, 17]

solution = chinese_remainder_theorem(remainders, moduli)
print(f"Solution: {solution}")

# Verification
print("\nVerification:")
print(f"{solution} mod 5 = {solution % 5}")   # Should be 2
print(f"{solution} mod 11 = {solution % 11}") # Should be 3
print(f"{solution} mod 17 = {solution % 17}") # Should be 5