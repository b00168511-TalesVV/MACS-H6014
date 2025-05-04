import math

N = 2**11

target_prob = 0.75

p_no_collision = 1.0
for n in range(1, N + 1):
    p_no_collision *= (1 - (n - 1) / N)
    if 1 - p_no_collision >= target_prob:
        print(f"Number of secrets needed for 75% collision probability: {n}")
        break
