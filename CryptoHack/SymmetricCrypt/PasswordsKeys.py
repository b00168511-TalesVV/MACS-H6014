import hashlib
import requests
from Crypto.Cipher import AES

BASE_URL = 'https://aes.cryptohack.org/passwords_as_keys'

def get_ciphertext():
    resp = requests.get(f'{BASE_URL}/encrypt_flag/')
    resp.raise_for_status()
    return resp.json()['ciphertext']

def load_wordlist():
    url = (
        'https://gist.githubusercontent.com/wchargin/8927565'
        '/raw/d9783627c731268fb2935a731a618aa8e95cf465/words'
    )
    resp = requests.get(url)
    resp.raise_for_status()
   
    return [w.strip() for w in resp.text.splitlines() if w.strip()]

def try_decrypt(cipher_hex, key_bytes):
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    ct = bytes.fromhex(cipher_hex)
    pt = cipher.decrypt(ct)
    try:
        s = pt.decode('utf-8')
    except UnicodeDecodeError:
        return None

    if s.startswith('crypto{') and s.rstrip().endswith('}'):
        return s.rstrip('\x00')  
    return None

def main():
    print('[*] Fetching ciphertext…')
    cipher_hex = get_ciphertext()
    print(f'    ciphertext = {cipher_hex}')

    print('[*] Loading wordlist…')
    words = load_wordlist()
    print(f'    {len(words)} candidate passwords loaded')

    print('[*] Brute-forcing…')
    for i, word in enumerate(words, 1):
        key = hashlib.md5(word.encode('utf-8')).digest()
        flag = try_decrypt(cipher_hex, key)
        if flag:
            print(f'[+] Found flag with password "{word}":\n    {flag}')
            return

        if i % 10000 == 0:
            print(f'    Tried {i} passwords…')

    print('[-] Flag not found.')

if __name__ == '__main__':
    main()
