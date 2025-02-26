def xor_string(input_string, xor_value):
    # XOR each character's Unicode value with the given integer
    result = ''.join(chr(ord(char) ^ xor_value) for char in input_string)
    return result

# Example input string (you would replace this with the actual 'label' string)
input_string = "label"
xor_value = 13

# XOR the string and get the result
new_string = xor_string(input_string, xor_value)

# Print the result in the required flag format
flag = f"crypto{{{new_string}}}"
print(flag)