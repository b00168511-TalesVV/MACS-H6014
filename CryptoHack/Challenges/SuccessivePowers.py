from math import gcd

a = [588, 665, 216, 113, 642, 4, 836, 114, 851, 492, 819, 237]

d = 0
for i in range(1, len(a) - 1):
    val = a[i-1] * a[i+1] - a[i]**2
    d = abs(val) if d == 0 else gcd(d, abs(val))

p = d

def modinv(x, m):
    return pow(x, m-2, m)

x = a[1] * modinv(a[0], p) % p

print(f"Recovered prime p = {p}")
print(f"Recovered base x = {x}")
