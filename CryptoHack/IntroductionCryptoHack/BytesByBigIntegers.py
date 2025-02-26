from Crypto.Util.number import long_to_bytes

num = 11515195063862318899931685488813747395775516287289682636499965282714637259206269
message = long_to_bytes(num)  # Convert integer to bytes
print(message.decode())  # Decode bytes to string