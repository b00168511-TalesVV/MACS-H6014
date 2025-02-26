# Function to XOR data with a key
def xor_with_key(data, key):
    return bytes([d ^ key[i % len(key)] for i, d in enumerate(data)])

# Given encrypted hex string
encrypted_hex = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"

# Decode from hex to bytes
encrypted_data = bytes.fromhex(encrypted_hex)
print(encrypted_data)

# Known flag start (part of the flag format)
known_flag_start = "crypto{"

# XOR the known flag start with the encrypted data to find the key
key = [encrypted_data[i] ^ ord(known_flag_start[i]) for i in range(len(known_flag_start))]
last_bit = [encrypted_data[len(encrypted_data)-1] ^ ord("}")]
key.append(last_bit.pop())

# Decrypt the entire message using the discovered key
decrypted_data = xor_with_key(encrypted_data, key)

# Convert the decrypted bytes back to text
decrypted_text = decrypted_data.decode('utf-8', errors='ignore')

# Print the decrypted flag
print(decrypted_text)