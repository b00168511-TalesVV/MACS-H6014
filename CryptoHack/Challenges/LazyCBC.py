import requests, binascii

BASE = "https://aes.cryptohack.org/lazy_cbc"

zero_block = "00" * 16
r = requests.get(f"{BASE}/encrypt/{zero_block}/")
C0 = r.json()["ciphertext"]

payload = zero_block + C0
r2 = requests.get(f"{BASE}/receive/{payload}/")
err = r2.json()["error"]

decrypted_hex = err.split(": ")[1]

key_hex = decrypted_hex[-32:]

r3 = requests.get(f"{BASE}/get_flag/{key_hex}/")
flag_hex = r3.json()["plaintext"]
flag = binascii.unhexlify(flag_hex).decode()
print("FLAG =", flag)
