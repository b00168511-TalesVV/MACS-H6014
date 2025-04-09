from pwn import *
import json
import base64
import codecs
from Crypto.Util.number import long_to_bytes

r = remote('socket.cryptohack.org', 13377, level='debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

def decode(encoding, encoded_value):
    if encoding == "base64":
        return base64.b64decode(encoded_value).decode('utf-8')
    elif encoding == "hex":
        return bytes.fromhex(encoded_value).decode('utf-8')
    elif encoding == "rot13":
        return codecs.decode(encoded_value, 'rot_13')
    elif encoding == "bigint":
        hex_str = encoded_value[2:]  # Remove '0x' prefix
        return long_to_bytes(int(hex_str, 16)).decode('utf-8')
    elif encoding == "utf-8":
        return ''.join(chr(c) for c in encoded_value)
    else:
        raise ValueError(f"Unknown encoding type: {encoding}")

for _ in range(100):
    received = json_recv()
    encoding_type = received["type"]
    encoded_value = received["encoded"]
    log.info(f"Received type: {encoding_type}, encoded value: {encoded_value}")
    
    decoded = decode(encoding_type, encoded_value)
    log.success(f"Decoded: {decoded}")
    
    to_send = {
        "decoded": decoded
    }
    json_send(to_send)

# After 100 levels, receive the flag
flag_response = json_recv()
log.success(f"Flag: {flag_response['flag']}")