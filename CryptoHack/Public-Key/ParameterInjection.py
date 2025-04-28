import socket
import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

HOST = 'socket.cryptohack.org'
PORT = 13371


def recv_line(sock):

    buf = b''
    while True:
        ch = sock.recv(1)
        if not ch:
            raise ConnectionError("Socket closed")
        if ch == b'\n':
            break
        buf += ch
    return buf.decode('utf-8', errors='ignore')


def recv_json(sock):
    while True:
        line = recv_line(sock).strip()
        if not line or '{' not in line:
            continue
        j = line[line.find('{'):]
        try:
            return json.loads(j)
        except json.JSONDecodeError:
            continue 


def send_json(sock, obj):
    data = (json.dumps(obj) + '\n').encode()
    sock.sendall(data)


def is_pkcs7_padded(data: bytes) -> bool:
    pad_len = data[-1]
    if pad_len < 1 or pad_len > AES.block_size:
        return False
    return data.endswith(bytes([pad_len]) * pad_len)


def main():
    # 1) Connect
    sock = socket.create_connection((HOST, PORT))

    # 2) Alice → Bob
    params = recv_json(sock)

    # 3) Inject g=1, A=1
    params['g'] = '0x1'
    params['A'] = '0x1'
    send_json(sock, params)

    # 4) Bob → Alice
    resp = recv_json(sock)


    resp['B'] = '0x1'
    send_json(sock, resp)

    msg = recv_json(sock)
    iv_hex = msg['iv']
    ct_hex = msg['encrypted_flag']

    key = hashlib.sha1(b"1").digest()[:16]

    iv = bytes.fromhex(iv_hex)
    ct = bytes.fromhex(ct_hex)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = cipher.decrypt(ct)

    if is_pkcs7_padded(pt):
        pt = unpad(pt, AES.block_size)

    print(pt.decode('ascii'))


if __name__ == '__main__':
    main()
