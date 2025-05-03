import json, socket

#STEP 1
x_bing = 0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531
y_bing = 0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A
n = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551

#STEP2
d = 2

#STEP3
inv_d = pow(d, -1, n)

#STEP4
p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
a = p - 3

def inv_mod(x, m): return pow(x, -1, m)

def ec_add(P, Q):
    if P is None: return Q
    if Q is None: return P
    x1,y1 = P; x2,y2 = Q
    if x1==x2 and (y1+y2) % p == 0:
        return None
    if (x1,y1) != (x2,y2):
        m = ((y2-y1) * inv_mod(x2-x1, p)) % p
    else:
        m = ((3*x1*x1 + a) * inv_mod(2*y1, p)) % p
    x3 = (m*m - x1 - x2) % p
    y3 = (m*(x1 - x3) - y1) % p
    return (x3,y3)

def ec_mul(k, P):
    R = None
    Q = P
    while k:
        if k & 1:
            R = ec_add(R, Q)
        Q = ec_add(Q, Q)
        k >>= 1
    return R

P_bing = (x_bing, y_bing)
g = ec_mul(inv_d, P_bing)
gx, gy = g

#STEP 5
packet = {
    "private_key": d,
    "host":        "ignored.when.Q.matches",
    "curve":       "secp256r1",
    "generator":   [gx, gy]
}

s = socket.create_connection(("socket.cryptohack.org", 13382))
s.sendall(json.dumps(packet).encode() + b"\n")
resp = s.recv(4096)
print(resp.decode())
s.close()
