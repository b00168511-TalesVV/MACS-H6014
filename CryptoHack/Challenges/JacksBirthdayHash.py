import math

bits = 11
p = 1 / (2 ** bits)
n = math.log(0.5) / math.log(1 - p)

print(f"Number of hashes needed: {n:.2f}")
