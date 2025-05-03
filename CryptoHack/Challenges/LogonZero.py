#!/usr/bin/env python3
import socket, json

HOST = "socket.cryptohack.org"
PORT = 13399

def send_cmd(s, obj):
    s.sendall((json.dumps(obj) + "\n").encode())
    return json.loads(s.recv(4096).decode())

def main():
    with socket.create_connection((HOST, PORT)) as s:
        # read the "Please authenticate..." banner
        print(s.recv(4096).decode(), end="")

        zero_token = "00" * 28  # 28 bytes of 0x00 in hex

        for attempt in range(1, 2000):
            # 1) rotate to a fresh random CFB8 key
            resp = send_cmd(s, {"option": "reset_connection"})
            # (resp == {'msg': 'Connection has been reset.'})

            # 2) submit the all‐zeros token
            resp = send_cmd(s, {
                "option": "reset_password",
                "token": zero_token
            })
            # (resp == {'msg': 'Password has been correctly reset.'})

            # 3) try to log in with the empty password
            auth = send_cmd(s, {
                "option": "authenticate",
                "password": ""
            })

            if auth["msg"].startswith("Welcome admin"):
                print("[+] Got it on try #%d!" % attempt)
                print(auth["msg"])
                break
            else:
                # wrong password – try again
                print(f"[-] Attempt #{attempt}: {auth['msg']}")
        else:
            print("[-] Didn’t hit the 1/256 case in 2000 tries – try increasing the loop limit.")

if __name__ == "__main__":
    main()
