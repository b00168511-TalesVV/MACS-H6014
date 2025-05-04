import socket
import json
import ast

HOST = 'socket.cryptohack.org'
PORT = 13411


q = 0x10001
n = 64

def solve_gauss_mod(A, y, q):

    M = [row[:] + [y_i] for row, y_i in zip(A, y)]
    row = 0
    for col in range(n):

        pivot = None
        for r in range(row, n):
            if M[r][col] % q != 0:
                pivot = r
                break
        if pivot is None:
            continue

        M[row], M[pivot] = M[pivot], M[row]

        inv_piv = pow(M[row][col], -1, q)
        M[row] = [(v * inv_piv) % q for v in M[row]]

        for r in range(n):
            if r != row and M[r][col] != 0:
                factor = M[r][col]
                M[r] = [
                    (M[r][c] - factor * M[row][c]) % q
                    for c in range(n + 1)
                ]
        row += 1
        if row == n:
            break

    return [M[i][-1] for i in range(n)]

def main():

    sock = socket.create_connection((HOST, PORT))
    f_in  = sock.makefile('r', encoding='utf-8', newline='\n')
    f_out = sock.makefile('w', encoding='utf-8', newline='\n')

    banner = f_in.readline()
    print(banner, end='')

    A_list, b_list = [], []
    for _ in range(n):
        f_out.write(json.dumps({"option": "encrypt", "message": 0}) + "\n")
        f_out.flush()

        resp = json.loads(f_in.readline())
        A = ast.literal_eval(resp["A"])
        A = [int(x) for x in A]
        b = int(resp["b"])

        A_list.append(A)
        b_list.append(b)

    S = solve_gauss_mod(A_list, b_list, q)

    flag_bytes = []
    idx = 0
    while True:
        f_out.write(json.dumps({"option": "get_flag", "index": idx}) + "\n")
        f_out.flush()

        resp = json.loads(f_in.readline())
        if "error" in resp:
            break

        A = ast.literal_eval(resp["A"])
        A = [int(x) for x in A]
        b = int(resp["b"])

        dot = sum(A[i] * S[i] for i in range(n)) % q
        m = (b - dot) % q

        flag_bytes.append(m)
        idx += 1

    flag = ''.join(chr(b) for b in flag_bytes)
    print("Recovered flag:", flag)

if __name__ == "__main__":
    main()
