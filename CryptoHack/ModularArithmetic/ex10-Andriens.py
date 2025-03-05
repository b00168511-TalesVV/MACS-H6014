a = 288260533169915
p = 1007621497415251

# Load and clean the ciphertext (replace spaces with commas)
with open("output.txt", "r") as f:
    content = f.read().replace("  ", ", ")  # Fix spaces between numbers
    ciphertext = eval(content)

def decrypt_flag(ciphertext):
    binary = ""
    for c in ciphertext:
        if c < p // 2:
            binary += "1"
        else:
            binary += "0"
    
    # Ensure binary length is a multiple of 8
    padding = len(binary) % 8
    if padding != 0:
        binary = binary[:-padding]  # Remove incomplete byte
    
    flag = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        flag += chr(int(byte, 2))
    return flag

flag = decrypt_flag(ciphertext)
print("Recovered flag:", flag)