import numpy as np

def load_data():
 
    pk = np.loadtxt("public_key_Nativity.txt", dtype=int)
    ct = np.loadtxt("ciphertexts_Nativity.txt", dtype=int)
    return pk, ct

def nullspace_mod2(A):

    A = A.copy() % 2
    rows, cols = A.shape
    pivots = []
    row = 0

    for col in range(cols):
        # find a pivot
        for r in range(row, rows):
            if A[r, col]:
                A[[row, r]] = A[[r, row]]  # swap
                break
        else:
            continue
        pivots.append(col)

        for r2 in range(rows):
            if r2 != row and A[r2, col]:
                A[r2, :] ^= A[row, :]
        row += 1
        if row == rows:
            break


    free_cols = [c for c in range(cols) if c not in pivots]
    basis = []

    for free in free_cols:
        x = np.zeros(cols, dtype=int)
        x[free] = 1
        for i, pv in enumerate(pivots):

            if A[i, free]:
                x[pv] = 1
        basis.append(x)
    return basis

def recover_flag(pk, ct):

    pk2 = pk % 2
    ct2 = ct % 2

    M = pk2.T 
    ns = nullspace_mod2(M)
    if len(ns) != 1:
        raise ValueError("expected a 1-dim nullspace, got %d basis vectors" % len(ns))
    sk2 = ns[0]

    bits = (ct2.dot(sk2) % 2).astype(int)

    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        val = int("".join(str(b) for b in byte), 2)
        chars.append(chr(val))
    return "".join(chars)

if __name__ == "__main__":
    pk, ct = load_data()
    flag = recover_flag(pk, ct)
    print(flag)
