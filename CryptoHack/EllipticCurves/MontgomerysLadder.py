# Montgomery Ladder implementation

p = 2**255 - 19

A = 486662

# Precomputed constant c = (A + 2) / 4 mod p
c = (A + 2) * pow(4, -1, p) % p 

# Base point x-coordinate
x1 = 9

def xDBL(X, Z):

    V1 = (X + Z) % p
    V2 = (X - Z) % p
    V1_sq = (V1 * V1) % p
    V2_sq = (V2 * V2) % p
    X2 = (V1_sq * V2_sq) % p
    V1_diff = (V1_sq - V2_sq) % p
    V3 = (c * V1_diff) % p
    V3 = (V3 + V2_sq) % p
    Z2 = (V1_diff * V3) % p
    return X2, Z2

def xADD(XP, ZP, XQ, ZQ, X_diff, Z_diff):

    V0 = (XP + ZP) % p
    V1 = (XQ - ZQ) % p
    V1 = (V1 * V0) % p
    V0 = (XP - ZP) % p
    V2 = (XQ + ZQ) % p
    V2 = (V2 * V0) % p
    V3 = (V1 + V2) % p
    V3_sq = (V3 * V3) % p
    V4 = (V1 - V2) % p
    V4_sq = (V4 * V4) % p
    X5 = (Z_diff * V3_sq) % p
    Z5 = (X_diff * V4_sq) % p
    return X5, Z5

def ladder(x1, k):
    # Initialize R0 = P, R1 = 2P in projective coords
    X0, Z0 = x1, 1
    X1, Z1 = xDBL(X0, Z0)

    for bit in bin(k)[3:]:
        if bit == '0':
            X1, Z1 = xADD(X0, Z0, X1, Z1, x1, 1)
            X0, Z0 = xDBL(X0, Z0)
        else:
            X0, Z0 = xADD(X0, Z0, X1, Z1, x1, 1)
            X1, Z1 = xDBL(X1, Z1)
    return X0, Z0

if __name__ == "__main__":

    k_hex = "1337c0decafe"
    k = int(k_hex, 16)

    XQ, ZQ = ladder(x1, k)

    xQ = (XQ * pow(ZQ, -1, p)) % p

    print("Q.x =", xQ)
