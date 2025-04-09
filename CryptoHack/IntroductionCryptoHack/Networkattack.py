
from pwn import *  
import json

HOST = "socket.cryptohack.org"
PORT = 11112

r = remote(HOST, PORT)


def json_recv():
    line = r.readline()
    return json.loads(line.decode())


def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)


# Read initial server messages (optional, for debugging)
print(r.readline())
print(r.readline())
print(r.readline())
print(r.readline())

# Send the required JSON object
request = {
    "buy": "flag"
}
json_send(request)

# Receive and print the response
response = json_recv()
print(response)

# Close the connection
r.close()