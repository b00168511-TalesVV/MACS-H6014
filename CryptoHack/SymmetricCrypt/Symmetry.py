import requests
from itertools import zip_longest

BASE = "https://aes.cryptohack.org/symmetry"

# 1) get the encrypted flag
r = requests.get(f"{BASE}/encrypt_flag/")
ivct = r.json()["ciphertext"]
iv_hex, ct_flag_hex = ivct[:32], ivct[32:]

# 2) get the keystream by encrypting zeros
flag_len = len(ct_flag_hex) // 2
zeros = "00" * flag_len
r2 = requests.get(f"{BASE}/encrypt/{zeros}/{iv_hex}/")
keystream_hex = r2.json()["ciphertext"]

# 3) XOR to recover the flag
flag_bytes = bytes(
    int(a, 16) ^ int(b, 16)
    for a, b in zip_longest(
        (keystream_hex[i:i+2] for i in range(0,len(keystream_hex),2)),
        (ct_flag_hex[i:i+2]    for i in range(0,len(ct_flag_hex),2)),
        fillvalue="00"
    )
)
print(flag_bytes.decode())
