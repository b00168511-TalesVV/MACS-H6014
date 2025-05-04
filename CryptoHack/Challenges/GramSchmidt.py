import numpy as np

def gram_schmidt(vectors):
    u = []
    for v in vectors:
        w = v.copy().astype(float)
        for uj in u:
            mu = np.dot(v, uj) / np.dot(uj, uj)
            w = w - mu * uj
        u.append(w)
    return u

v1 = np.array([4, 1, 3, -1], dtype=float)
v2 = np.array([2, 1, -3, 4], dtype=float)
v3 = np.array([1, 0, -2, 7], dtype=float)
v4 = np.array([6, 2, 9, -5], dtype=float)

vectors = [v1, v2, v3, v4]
u = gram_schmidt(vectors)

u4_second = u[3][1]
print(f"u4 second component: {u4_second:.5g}")
