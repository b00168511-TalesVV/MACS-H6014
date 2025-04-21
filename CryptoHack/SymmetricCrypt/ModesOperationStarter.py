import requests
# Encrypted flag from the previous step
encrypted_flag = "bf791ff22629657bedc29428674f686758cc40d847834a4665a205bf540fbdfb"

# API URL for decrypting the ciphertext
url_decrypt = f"https://aes.cryptohack.org/block_cipher_starter/decrypt/{encrypted_flag}/"

# Send GET request to decrypt the ciphertext
response = requests.get(url_decrypt)

# Check if the request was successful
if response.status_code == 200:
    decrypted_flag = response.json().get("plaintext")
    print(f"Decrypted Flag (Hex): {decrypted_flag}")
else:
    print("Failed to decrypt the flag.")


decrypted_flag_hex = "63727970746f7b626c30636b5f633170683372355f3472335f663435375f217d"

# Convert hex to bytes and then decode to string
decrypted_flag = bytes.fromhex(decrypted_flag_hex).decode('utf-8')

print(f"Decrypted Flag: {decrypted_flag}")