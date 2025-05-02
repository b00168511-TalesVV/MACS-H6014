import requests
from binascii import unhexlify

def decrypt_block(block_hex):
    url = f"https://aes.cryptohack.org/ecbcbcwtf/decrypt/{block_hex}/"
    r = requests.get(url)
    r.raise_for_status()
    plaintext_hex = r.json().get("plaintext")
    if plaintext_hex is None:
        raise RuntimeError(f"Oracle error: {r.json().get('error')}")
    return unhexlify(plaintext_hex)

def main():
    # 1. Retrieve CBC-encrypted flag (IV + ciphertext)
    r = requests.get("https://aes.cryptohack.org/ecbcbcwtf/encrypt_flag/")
    r.raise_for_status()
    ciphertext_hex = r.json()["ciphertext"]

    # 2. Split into IV and 16-byte blocks
    iv = unhexlify(ciphertext_hex[:32])
    blocks = [ciphertext_hex[i:i+32] for i in range(32, len(ciphertext_hex), 32)]

    # 3. Decrypt each block and unchain via XOR
    plaintext = b""
    prev = iv
    for block_hex in blocks:
        decrypted = decrypt_block(block_hex)
        pt_block = bytes(a ^ b for a, b in zip(decrypted, prev))
        plaintext += pt_block
        prev = unhexlify(block_hex)

    # 4. Decode plaintext directly (flag is exactly block-aligned, no padding)
    flag = plaintext.decode('ascii')
    print("Recovered flag:", flag)

if __name__ == "__main__":
    main()
