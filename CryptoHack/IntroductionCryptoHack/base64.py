import base64

hex_string = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"
byte_data = bytes.fromhex(hex_string)  # Convert hex to bytes
base64_encoded = base64.b64encode(byte_data)  # Encode bytes to Base64
print(base64_encoded.decode())  # Convert bytes to a readable string