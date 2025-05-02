#!/usr/bin/env python3
"""
Solver for the CryptoHack Bean Counter challenge with automatic OCR and flag saving.
1. Download the encrypted PNG
2. Recover the fixed CTR keystream via the PNG header
3. Decrypt the image
4. OCR the image to read the flag
5. Save the flag to flag.txt
"""
import requests
from io import BytesIO
from PIL import Image
import pytesseract

# Endpoint providing the encrypted PNG data
encrypt_url = 'https://aes.cryptohack.org/bean_counter/encrypt/'


def get_ciphertext():
    """
    Fetch encrypted data (hex string) from the challenge server and decode to bytes.
    """
    resp = requests.get(encrypt_url)
    resp.raise_for_status()
    return bytes.fromhex(resp.json()['encrypted'])


def derive_keystream(ct0):
    """
    Use the known PNG signature and IHDR header in the first 16 bytes to recover the keystream block.
    """
    pt0 = bytes([
        0x89,0x50,0x4E,0x47,  # .PNG
        0x0D,0x0A,0x1A,0x0A,  # \r\n\x1a\n
        0x00,0x00,0x00,0x0D,  # chunk length (13)
        0x49,0x48,0x44,0x52   # 'IHDR'
    ])
    return bytes(c ^ p for c, p in zip(ct0, pt0))


def decrypt(ciphertext, ks):
    """
    XOR the ciphertext with the repeated keystream to recover plaintext bytes.
    """
    out = bytearray()
    for i in range(0, len(ciphertext), len(ks)):
        block = ciphertext[i:i+len(ks)]
        out.extend(b ^ ks[j] for j, b in enumerate(block))
    return bytes(out)


def ocr_flag(png_bytes):
    """
    Run OCR on the decrypted PNG bytes to extract the flag.
    """
    img = Image.open(BytesIO(png_bytes))
    text = pytesseract.image_to_string(img).strip()
    for token in text.split():
        if token.startswith('crypto{') and token.endswith('}'):
            return token
    return None


def main():
    # 1) Fetch ciphertext
    ct = get_ciphertext()

    # 2) Derive the keystream from first block
    ks = derive_keystream(ct[:16])

    # 3) Decrypt the entire PNG
    plain = decrypt(ct, ks)

    # 4) Save decrypted image for inspection (optional)
    with open('bean_flag.png','wb') as f:
        f.write(plain)
    print("Decrypted image saved to bean_flag.png")

    # 5) OCR to extract the flag
    flag = ocr_flag(plain)
    if not flag:
        print('Flag not found via OCR; please open bean_flag.png to read it.')
        return

    # 6) Save the flag to a text file
    with open('flag.txt', 'w') as f:
        f.write(flag + '\n')
    print(f"Flag found and saved to flag.txt: {flag}")


if __name__ == '__main__':
    main()
