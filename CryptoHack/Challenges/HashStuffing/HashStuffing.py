#!/usr/bin/env python3
import socket
import json
import os
import sys

# import the hash internals from source.py (make sure source.py is in the same directory)
from source import (
    BLOCK_SIZE,
    W_bytes, X_bytes, Y_bytes, Z_bytes,
    pad, blocks, xor, rotate_left, rotate_right, scramble_block
)

HOST = "socket.cryptohack.org"
PORT = 13405

def mix_in(block: bytes, idx: int) -> bytes:
    """
    f_i(b) = scramble_block(b), then for idx times:
      rotate_right by (idx+11), xor X_bytes, rotate_left by (idx+6)
    """
    v = scramble_block(block)
    for _ in range(idx):
        v = rotate_right(v, idx + 11)
        v = xor(X_bytes, v)
        v = rotate_left(v, idx + 6)
    return v

def mix_in_inv_target(target: bytes, idx: int) -> bytes:
    """
    Invert mix_in for a given idx, only used for idx=1 here.
    """
    v = target
    # invert the inner loop in reverse
    for _ in range(idx):
        # invert rotate_left(idx+6) → rotate_right(idx+6)
        v = rotate_right(v, idx + 6)
        # invert xor(X_bytes)
        v = xor(X_bytes, v)
        # invert rotate_right(idx+11) → rotate_left(idx+11)
        v = rotate_left(v, idx + 11)

    # invert scramble_block (40 rounds of xor(W), rotl 6, xor(X), rotr 17)
    for _ in range(40):
        v = rotate_left(v, 17)    # invert rotr(17)
        v = xor(X_bytes, v)       # invert xor(X)
        v = rotate_right(v, 6)    # invert rotl(6)
        v = xor(W_bytes, v)       # invert xor(W)
    return v

def cryptohash(msg: bytes) -> str:
    """
    The server's hash: start with Y⊕Z, pad & split into 256-bit blocks,
    then XOR in mix_in(block, index) for each block.
    """
    state = xor(Y_bytes, Z_bytes)
    data = pad(msg)
    for i, blk in enumerate(blocks(data)):
        state = xor(state, mix_in(blk, i))
    return state.hex()

def make_collision():
    """
    Build two distinct 2-block messages that collide:
      pick b1,b2,c1 at random, then solve for c2 so that
        mix_in(b1,0)^mix_in(b2,1) == mix_in(c1,0)^mix_in(c2,1)
    """
    # pick two random blocks for the first message
    b1 = os.urandom(BLOCK_SIZE)
    b2 = os.urandom(BLOCK_SIZE)

    # pick a different first block for the second message
    while True:
        c1 = os.urandom(BLOCK_SIZE)
        if c1 != b1:
            break

    # compute the mixed values
    m0 = mix_in(b1, 0)
    m1 = mix_in(b2, 1)
    mc0 = mix_in(c1, 0)

    # we need mc1 so that m0 ^ m1 == mc0 ^ mc1
    mc1_target = xor(xor(m0, m1), mc0)
    # invert mix_in at index=1 to find c2
    c2 = mix_in_inv_target(mc1_target, 1)

    msg1 = b1 + b2
    msg2 = c1 + c2

    # sanity checks
    assert msg1 != msg2
    assert cryptohash(msg1) == cryptohash(msg2)
    return msg1, msg2

def recv_json(sock: socket.socket):
    data = b""
    while not data.endswith(b"\n"):
        chunk = sock.recv(4096)
        if not chunk:
            raise ConnectionError("Connection lost")
        data += chunk
    return json.loads(data.decode())

def send_json(sock: socket.socket, obj):
    sock.sendall((json.dumps(obj) + "\n").encode())

def main():
    # generate our colliding pair
    m1, m2 = make_collision()
    hex1, hex2 = m1.hex(), m2.hex()

    # connect and talk to the service
    with socket.create_connection((HOST, PORT)) as s:
        # read and print the welcome message
        print(s.recv(4096).decode(), end="")

        # send both messages in one JSON packet
        packet = {"m1": hex1, "m2": hex2}
        print("[*] Sending collision pair...")
        send_json(s, packet)

        # receive response
        resp = recv_json(s)
        print(resp)
        if "flag" in resp:
            print("\nFLAG:", resp["flag"])
        else:
            print("No flag returned. Response above.")

if __name__ == "__main__":
    main()
