# Define modular exponentiation function
def mod_exp(base, exp, mod):
    return pow(base, exp, mod)  # Built-in Python function for efficient modular exponentiation

# Given prime modulus
p1 = 17
p2 = 65537

# Calculations using Fermat's Little Theorem
print(f"3^17 mod 17 = {mod_exp(3, 17, p1)}")
print(f"5^17 mod 17 = {mod_exp(5, 17, p1)}")
print(f"7^16 mod 17 = {mod_exp(7, 16, p1)}")

# Large exponentiation case
large_base = 273246787654
large_exp = 65536
print(f"{large_base}^{large_exp} mod {p2} = {mod_exp(large_base, large_exp, p2)}")
