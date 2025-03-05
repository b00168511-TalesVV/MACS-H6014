a = 3
m = 13

# Using Fermat's Little Theorem
inverse = pow(a, m - 2, m)
print(f"Multiplicative inverse of {a} modulo {m} is {inverse}")

