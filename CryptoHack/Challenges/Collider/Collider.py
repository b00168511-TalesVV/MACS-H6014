import socket
import json

HOST = 'socket.cryptohack.org'
PORT = 13389

def recv_json(sock):
    """Read a line from the socket and decode it as JSON."""
    line = sock.recv(4096)
    if not line:
        raise ConnectionError("Server closed connection")
    return json.loads(line.decode('utf-8', errors='ignore'))

def send_json(sock, obj):
    """Send a JSON object, terminated by newline."""
    data = json.dumps(obj, separators=(',', ':')).encode('utf-8') + b'\n'
    sock.sendall(data)

def main():
    # load your two colliding messages
    with open('msg1.bin', 'rb') as f:
        m1 = f.read()
    with open('msg2.bin', 'rb') as f:
        m2 = f.read()

    # JSON only supports text, so we re‐encode raw bytes via Latin-1 lossless mapping
    s1 = m1.hex()
    s2 = m2.hex()

    # connect
    with socket.create_connection((HOST, PORT)) as sock:
        # read server’s greeting / prompt
        greeting = sock.recv(4096).decode('utf-8', errors='ignore')
        print(greeting.strip())

        # send first document
        print("[*] Sending first document...")
        send_json(sock, {'document': s1})
        resp1 = recv_json(sock)
        print("[<] ", resp1)

        # send second (colliding) document
        print("[*] Sending second document...")
        send_json(sock, {'document': s2})
        resp2 = recv_json(sock)
        print("[<] ", resp2)

        # one of these responses should include the flag
        if 'flag' in resp2:
            print("FLAG:", resp2['flag'])

if __name__ == '__main__':
    main()
