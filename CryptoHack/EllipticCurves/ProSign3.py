import socket
import json
import time
import hashlib
from Crypto.Util.number import bytes_to_long, inverse
from ecdsa.ecdsa import generator_192

HOST = 'socket.cryptohack.org'
PORT = 13381

g = generator_192
n_curve = g.order()

def recv_text(s):
    data = b''
    while not data.endswith(b'\n'):
        chunk = s.recv(4096)
        if not chunk:
            raise ConnectionError("Connection closed by remote host")
        data += chunk
    return data.decode()

def recv_json(s):
    data = b''
    while not data.endswith(b'\n'):
        chunk = s.recv(4096)
        if not chunk:
            raise ConnectionError("Connection closed by remote host")
        data += chunk
    return json.loads(data.decode())

def send_json(s, obj):
    s.sendall((json.dumps(obj) + '\n').encode())
    return recv_json(s)

def connect():
    s = socket.create_connection((HOST, PORT))
    banner = recv_text(s)
    print(banner, end='') 
    return s

def main():
    s = connect()

    while True:
        try:
            reply = send_json(s, {"option": "sign_time"})
        except (ConnectionError, json.JSONDecodeError) as e:

            print(f"Connection error or bad JSON: {e!r}. Reconnecting...")
            try:
                s.close()
            except:
                pass
            s = connect()
            continue

        if 'msg' not in reply:
            print("Server error reply:", reply)
            time.sleep(0.2)
            continue

        msg = reply['msg']
        sec = int(msg.split(':')[-1])
        print(f"sign_time → seconds = {sec}")
        if sec == 2:
            print("Got seconds=2; reply =", reply)
            break

        time.sleep(0.1)

    r = int(reply['r'], 16)
    s_sig = int(reply['s'], 16)
    h = bytes_to_long(hashlib.sha1(msg.encode()).digest())
    k = 1  
    d = (s_sig * k - h) * inverse(r, n_curve) % n_curve
    print(f"Key Recovered d = {d}")

    m2 = "unlock"
    h2 = bytes_to_long(hashlib.sha1(m2.encode()).digest())
    k2 = 1
    R2 = g * k2
    r2 = R2.x() % n_curve
    s2 = (inverse(k2, n_curve) * (h2 + d * r2)) % n_curve

    result = send_json(s, {
        "option": "verify",
        "msg": m2,
        "r": hex(r2),
        "s": hex(s2)
    })
    print("Flag response:", result)

if __name__ == '__main__':
    main()
