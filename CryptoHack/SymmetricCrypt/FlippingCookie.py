import requests
from binascii import unhexlify, hexlify

BASE = "https://aes.cryptohack.org/flipping_cookie"

# 1. Fetch your cookie (IV||ciphertext in hex)
r = requests.get(f"{BASE}/get_cookie/")
blob = r.json()["cookie"]
iv_hex, ct_hex = blob[:32], blob[32:]

# 2. Prepare deltas for positions 6..10
deltas = {
    6:  0x46 ^ 0x54,
    7:  0x61 ^ 0x72,
    8:  0x6c ^ 0x75,
    9:  0x73 ^ 0x65,
    10: 0x65 ^ 0x3b,
}

# 3. Flip bits in the IV
iv = bytearray(unhexlify(iv_hex))
for pos, d in deltas.items():
    iv[pos] ^= d
iv_mod = hexlify(iv).decode()

# 4. Send modified IV + original ciphertext
check = requests.get(f"{BASE}/check_admin/{ct_hex}/{iv_mod}/")
print(check.json())
# recovers the flag
