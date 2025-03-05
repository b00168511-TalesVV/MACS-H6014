def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Test case
print(gcd(12, 8))  # Should print 4

# Compute gcd(66528, 52920)
print(gcd(66528, 52920))