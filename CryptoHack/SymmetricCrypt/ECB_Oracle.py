import requests
import string

BASE = 'https://aes.cryptohack.org'
ENDPOINT = '/ecb_oracle/encrypt/'

def encrypt(data_bytes: bytes) -> bytes:
    hex_payload = data_bytes.hex()
    r = requests.get(f"{BASE}{ENDPOINT}{hex_payload}/")
    r.raise_for_status()
    return bytes.fromhex(r.json()['ciphertext'])


def find_block_size() -> int:
    prev_len = len(encrypt(b"A")) 
    for i in range(2, 65): 
        L = len(encrypt(b"A" * i))
        if L != prev_len:
            return L - prev_len
    raise RuntimeError("Unable to determine block size")




def is_ecb(block_size: int) -> bool:
    ct = encrypt(b"A" * (block_size * 2))
    return ct[:block_size] == ct[block_size:block_size*2]

def recover_flag():
    block_size = find_block_size()
    print(f"[+] Detected block size: {block_size}")
    assert is_ecb(block_size), "Not using ECB mode!"

    known = b""

    for i in range(64):
        pad_len = (block_size - 1) - (len(known) % block_size)
        
        if pad_len == 0:
            prefix = b"A" * block_size
        else:
            prefix = b"A" * pad_len

        ct = encrypt(prefix)
        block_index = (len(prefix) + len(known)) // block_size
        target_block = ct[block_index * block_size:(block_index + 1) * block_size]

        # brute‐force the next byte
        found = False
        for c in (string.ascii_letters + string.digits + "_{}").encode():
            guess = prefix + known + bytes([c])
            gct = encrypt(guess)
            guess_block = gct[block_index * block_size:(block_index + 1) * block_size]
            if guess_block == target_block:
                known += bytes([c])
                print(f"[+] Found byte {bytes([c])!r}; flag so far: {known.decode()}")
                found = True
                break

        if not found:
            print("[!] No match—probably reached end of flag.")
            break
        if known.endswith(b"}"):
            break

    return known.decode()

if __name__ == "__main__":
    flag = recover_flag()
    print(f"\nRecovered flag: {flag}")
