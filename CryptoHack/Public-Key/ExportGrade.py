import socket, json, hashlib, math, random
from collections import Counter
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

HOST, PORT = 'socket.cryptohack.org', 13379

def recv_json_line(f):
    raw = f.readline()
    if not raw:
        raise ConnectionError("Connection closed")
    line = raw.strip()
    i = line.find('{')
    j = line.rfind('}')
    if i < 0 or j < 0:
        return recv_json_line(f)
    return json.loads(line[i:j+1])

def send_json(sock, obj):
    sock.sendall((json.dumps(obj) + '\n').encode())

def is_prime(n):
    if n<2: return False
    for a in (2,325,9375,28178,450775,9780504,1795265022):
        if n % a == 0:
            return n == a
    d, s = n-1, 0
    while not d&1:
        d >>= 1; s += 1
    for a in (2,325,9375,28178,450775,9780504,1795265022):
        x = pow(a, d, n)
        if x in (1, n-1):
            continue
        for _ in range(s-1):
            x = pow(x, 2, n)
            if x == n-1:
                break
        else:
            return False
    return True

def pollard_rho(n):
    if n%2==0: return 2
    if is_prime(n): return n
    while True:
        x = random.randrange(2, n-1)
        y, c, d = x, random.randrange(1, n-1), 1
        while d==1:
            x = (x*x + c) % n
            y = (y*y + c) % n
            y = (y*y + c) % n
            d = math.gcd(abs(x-y), n)
            if d==n:
                break
        if 1<d<n:
            return d

def factor_full(n):
    facs = []
    while n%2==0:
        facs.append(2); n//=2
    p = 3
    while p*p<=n and p<=100000:
        while n%p==0:
            facs.append(p); n//=p
        p+=2
    if n>1:
        if is_prime(n):
            facs.append(n)
        else:
            d = pollard_rho(n)
            facs += factor_full(d) + factor_full(n//d)
    return facs

def discrete_log_prime_power(g, h, p, q, e):
    pe = q**e
    g0 = pow(g, (p-1)//pe, p)
    h0 = pow(h, (p-1)//pe, p)
    m = int(math.isqrt(pe)) + 1
    table = {pow(g0, j, p): j for j in range(m)}
    inv_g0 = pow(g0, p-2, p)
    factor = pow(inv_g0, m, p)
    gamma = h0
    for i in range(m):
        if gamma in table:
            return (i*m + table[gamma]) % pe
        gamma = (gamma*factor) % p
    raise ValueError

def egcd(a,b):
    if b==0: return (a,1,0)
    g,x1,y1 = egcd(b, a%b)
    return (g, y1, x1 - (a//b)*y1)

def modinv(a,m):
    g,x,_ = egcd(a,m)
    if g!=1:
        raise ValueError
    return x % m

def crt(rems, mods):
    M = math.prod(mods)
    x = 0
    for r,m in zip(rems,mods):
        Mi = M//m
        x = (x + r*Mi*modinv(Mi,m)) % M
    return x

def pohlig_hellman(g, h, p):
    N = p-1
    facs = Counter(factor_full(N))
    rems, mods = [], []
    for q,e in facs.items():
        rems.append(discrete_log_prime_power(g,h,p,q,e))
        mods.append(q**e)
    return crt(rems, mods)

def main():
    sock = socket.create_connection((HOST, PORT))
    f = sock.makefile('r')

    # 1) force DH64 negotiation
    _ = recv_json_line(f)
    send_json(sock, {'supported':['DH64']})
    chosen = recv_json_line(f)
    send_json(sock, chosen)

    # 2) forward DH params and capture values
    params = recv_json_line(f)
    p = int(params['p'], 16); g = int(params['g'], 16); A = int(params['A'], 16)
    send_json(sock, params)
    resp = recv_json_line(f)
    B = int(resp['B'], 16)
    send_json(sock, resp)

    # 3) capture encrypted flag
    enc = recv_json_line(f)
    iv = bytes.fromhex(enc['iv'])
    ct = bytes.fromhex(enc['encrypted_flag'])

    # 4) recover shared secret via PH on 64-bit p
    a = pohlig_hellman(g, A, p)
    shared = pow(B, a, p)
    key = hashlib.sha1(str(shared).encode()).digest()[:16]

    # 5) decrypt, try unpad, fallback to raw
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = cipher.decrypt(ct)
    try:
        flag = unpad(pt, AES.block_size).decode('ascii')
    except ValueError:
        flag = pt.decode('ascii')

    print(flag)

if __name__ == '__main__':
    main()
