import hashlib
from Crypto.Cipher import AES
import binascii

p = 9739
a = 497
b = 1768

x_QA = 4726

nB = 6534

data = {
    'iv': 'cd9da9f1c60925922377ea952afc212c',
    'encrypted_flag': 'febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8'
}

# Helper functions
def inverse_mod(k, p):
    return pow(k, -1, p)

def point_add(P, Q, a, p):
    if P is None:
        return Q
    if Q is None:
        return P
    (x1, y1) = P
    (x2, y2) = Q
    if x1 == x2 and (y1 != y2 or y1 == 0):
        return None
    if P != Q:
        m = (y2 - y1) * inverse_mod(x2 - x1, p) % p
    else:
        m = (3 * x1 * x1 + a) * inverse_mod(2 * y1, p) % p
    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return (x3, y3)

def scalar_mult(k, P, a, p):
    R = None
    Q = P
    while k > 0:
        if k % 2 == 1:
            R = point_add(R, Q, a, p)
        Q = point_add(Q, Q, a, p)
        k //= 2
    return R

def recover_y(x, a, b, p):
    y_squared = (x**3 + a*x + b) % p
    y = pow(y_squared, (p+1)//4, p)
    return y, p - y

def decrypt_flag(shared_secret_x, iv_hex, ciphertext_hex):
    key = hashlib.sha1(str(shared_secret_x).encode()).digest()[:16]
    iv = binascii.unhexlify(iv_hex)
    ciphertext = binascii.unhexlify(ciphertext_hex)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted

# Step 1: Recover both possible y values
y1, y2 = recover_y(x_QA, a, b, p)
candidates = [(x_QA, y1), (x_QA, y2)]

# Step 2: Try both possible points
for idx, QA in enumerate(candidates):
    shared_secret = scalar_mult(nB, QA, a, p)
    if shared_secret is not None:
        x_shared, _ = shared_secret
        decrypted = decrypt_flag(x_shared, data['iv'], data['encrypted_flag'])
        try:

            flag = decrypted.decode('utf-8')
            if 'crypto' in flag:
                print(f"[+] Success with candidate {idx+1}!")
                print(flag)
                break
        except UnicodeDecodeError:

            continue
