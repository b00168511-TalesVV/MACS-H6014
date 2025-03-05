def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, u1, v1 = extended_gcd(b % a, a)
        u = v1 - (b // a) * u1
        v = u1
        return gcd, u, v

# Given values
p = 26513
q = 32321

# Compute extended GCD
gcd_val, u, v = extended_gcd(p, q)

print(f"gcd({p}, {q}) = {gcd_val}")
print(f"Values of u and v: u = {u}, v = {v}")
