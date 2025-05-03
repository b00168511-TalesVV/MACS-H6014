import requests
from Crypto.Util.Padding import unpad

BASE_URL = "https://aes.cryptohack.org"

def encrypt(key_hex: str, plaintext: bytes) -> bytes:

    url = f"{BASE_URL}/triple_des/encrypt/{key_hex}/{plaintext.hex()}/"
    resp = requests.get(url).json()
    return bytes.fromhex(resp["ciphertext"])

def encrypt_flag(key_hex: str) -> bytes:

    url = f"{BASE_URL}/triple_des/encrypt_flag/{key_hex}/"
    resp = requests.get(url).json()
    return bytes.fromhex(resp["ciphertext"])

def main():

    key = b"\x00" * 8 + b"\xFF" * 8
    key_hex = key.hex()

    flag_ct = encrypt_flag(key_hex)

    padded = encrypt(key_hex, flag_ct)

    flag = unpad(padded, 8).decode()
    print("Recovered flag:", flag)

if __name__ == "__main__":
    main()
