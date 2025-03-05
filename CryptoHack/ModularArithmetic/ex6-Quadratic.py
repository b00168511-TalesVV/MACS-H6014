# Function to calculate square roots modulo p
def find_square_root(x, p):
    for a in range(1, p):
        if (a * a) % p == x:
            return a
    return None  # No square root exists

# Modulo value
p = 29

# List of integers to check
ints = [14, 6, 11]

# Check each number to see if it is a quadratic residue modulo p
for x in ints:
    root = find_square_root(x, p)
    if root is not None:
        print(f"The square root of {x} mod {p} is {root}")
    else:
        print(f"{x} is a quadratic non-residue mod {p}")
