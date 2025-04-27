
# Requires: SageMath

import sys
from sage.all import (
    EllipticCurve, GF, discrete_log, Integer
)
from hashlib import sha1
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def main():

    p = 310717010502520989590157367261876774703
    a, b = 2, 3

    Fp = GF(p)
    E  = EllipticCurve(Fp, [a, b])

    Gx = 179210853392303317793440285562762725654
    Gy = 105268671499942631758568591033409611165
    G  = E(Gx, Gy)

    # Your ephemeral public P = n*G (printed in the challenge)
    Px = 280810182131414898730378982766101210916
    Py = 291506490768054478159835604632710368904
    Ppub = E(Px, Py)

    Bx = 272640099140026426377756188075937988094
    By = 51062462309521034358726608268084433317
    B  = E(Bx, By)

    iv_hex  = "07e2628b590095a5e332d397b8a59aa7"
    ct_hex  = "8220b7c47b36777a737f5ef9caa2814cf20c1c1ef496ec21a9b4833da24a008d0870d3ac3a6ad80065c138a2ed6136af"
    iv = bytes.fromhex(iv_hex)
    ct = bytes.fromhex(ct_hex)

    # 1. Compute the group
    N = E.order()
    print(f"Curve group order N = {N}")
    print("Factorization:", N.factor())

    # 2. Recover 
    print("Computing discrete_log(Ppub, G) …")
    n = discrete_log(Ppub, G, operation='+', ord=N)
    print(f"Recovered n = {n}")

    S = n * B
    ss = Integer(S[0])  

    # 4. Derive AES key from SHA-1(shared_secret) and decrypt
    key = sha1(str(ss).encode('ascii')).digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    flag = unpad(cipher.decrypt(ct), 16)

    print("Recovered flag:", flag.decode())

if __name__ == "__main__":
    main()
