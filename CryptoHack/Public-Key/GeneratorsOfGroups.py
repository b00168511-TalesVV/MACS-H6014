import sympy

def smallest_primitive_root(p):
    """
    Finds the smallest primitive root modulo p, 
    assuming p is a prime number.
    """
    # Factor p-1
    factors = sympy.factorint(p - 1)
    # Extract the distinct prime factors
    prime_factors = list(factors.keys())

    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in prime_factors):
            return g
    raise ValueError(f"No primitive root found for p = {p}")

if __name__ == "__main__":
    p = 28151
    g = smallest_primitive_root(p)
    print(f"The smallest primitive root modulo {p} is {g}.")
