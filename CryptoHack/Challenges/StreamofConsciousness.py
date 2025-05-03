import requests
import string
import sys

# ------------------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------------------
URL     = "https://aes.cryptohack.org/stream_consciousness/encrypt/"
N_FETCH = 600    # how many total requests to make
CRIBS   = [      # common words/phrases to try in crib-drag
    b" the ", b" and ", b" you ",
    b" is ", b" that ", b" in ",
    b" to ", b" of ", b" stream ",
    b" since ", b" years ", b" consciousness"
]

# ------------------------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------------------------
def fetch_ciphertexts(n):
    seen = set()
    for i in range(n):
        try:
            r = requests.get(URL, timeout=5)
            r.raise_for_status()
            c = r.json().get("ciphertext")
            if c:
                seen.add(c)
        except Exception as e:
            print(f"[!] fetch error #{i+1}: {e}", file=sys.stderr)
    return list(seen)

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def is_printable(bs: bytes) -> bool:
    return all(chr(b) in string.printable for b in bs)

# ------------------------------------------------------------------------------
# CRIB-DRAG
# ------------------------------------------------------------------------------
def crib_drag(xor_stream: bytes):
    print("\n=== Crib-drag results ===")
    for crib in CRIBS:
        print(f"\n[Crib] {crib!r}")
        for i in range(len(xor_stream) - len(crib) + 1):
            seg = xor_stream[i : i + len(crib)]
            out = bytes(s ^ c for s, c in zip(seg, crib))
            if is_printable(out):
                print(f"  Offset {i:3d}: {out!r}")

# ------------------------------------------------------------------------------
# MAIN FLOW
# ------------------------------------------------------------------------------
def main():
    # 1) collect ciphertexts
    print(f"[+] Fetching up to {N_FETCH} ciphertexts…")
    cts = fetch_ciphertexts(N_FETCH)
    print(f"[+] Got {len(cts)} unique ciphertexts.\n")

    # 2) pick two for crib-drag (show first few for index)
    for idx, c_hex in enumerate(cts[:8]):
        print(f"  [{idx}] len={len(bytes.fromhex(c_hex))}")
    i1, i2 = map(int, input("\nPick two indices to crib-drag (e.g. 0 1): ").split())
    c1 = bytes.fromhex(cts[i1])
    c2 = bytes.fromhex(cts[i2])

    # 3) do the XOR and crib-drag
    xor_stream = xor_bytes(c1, c2)
    print(f"\n[*] P1⊕P2 ({len(xor_stream)} bytes):\n{xor_stream}\n")
    crib_drag(xor_stream)

    # 4) once you've identified the full plaintext for c1, paste it:
    p1 = input(f"\nEnter the FULL recovered plaintext for ciphertext #{i1}: ").encode()
    if len(p1) != len(c1):
        print("[!] Warning: plaintext length mismatch!", file=sys.stderr)

    # 5) derive keystream
    ks = xor_bytes(c1, p1)
    print("[+] Keystream recovered.\n")

    # 6) decrypt everything and search for the flag
    print("[+] Decrypting all ciphertexts…")
    for idx, c_hex in enumerate(cts):
        ct = bytes.fromhex(c_hex)
        pt = xor_bytes(ct, ks[:len(ct)])
        try:
            s = pt.decode()
        except UnicodeDecodeError:
            continue
        if s.startswith("crypto{") and s.endswith("}"):
            print(f"\n=== FLAG FOUND in ciphertext #{idx} ===\n{s}")
            return

    print("\n[!] Flag not found—try a different recovered line or different pair.")

if __name__ == "__main__":
    main()
