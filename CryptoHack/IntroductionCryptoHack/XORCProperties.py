# Helper function to convert hex to bytes and XOR them
def xor_bytes(byte1, byte2):
    return bytes(a ^ b for a, b in zip(byte1, byte2))

# Given values
KEY1 = bytes.fromhex("a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313")
KEY2_XOR_KEY1 = bytes.fromhex("37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e")
KEY2_XOR_KEY3 = bytes.fromhex("c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1")
ENCRYPTED_FLAG = bytes.fromhex("04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf")

# Step 1: XOR KEY2 and KEY1 to recover KEY2
KEY2 = xor_bytes(KEY2_XOR_KEY1, KEY1)

# Step 2: XOR KEY3 and KEY2 to recover KEY3
KEY3 = xor_bytes(KEY2_XOR_KEY3, KEY2)

# Step 3: XOR everything to recover the FLAG
flag = xor_bytes(xor_bytes(ENCRYPTED_FLAG, KEY1), xor_bytes(KEY3, KEY2))

# Convert the final result to string (if it's text)
print(flag.decode('utf-8'))
