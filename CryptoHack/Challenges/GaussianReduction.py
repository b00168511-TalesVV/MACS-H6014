import math

def gauss_reduce(v1, v2):

    v1 = list(v1)
    v2 = list(v2)
    while True:
        if v2[0]**2 + v2[1]**2 < v1[0]**2 + v1[1]**2:
            v1, v2 = v2, v1

        dot12 = v1[0]*v2[0] + v1[1]*v2[1]
        dot11 = v1[0]*v1[0] + v1[1]*v1[1]
        m = int(round(dot12 / dot11))

        if m == 0:
            break

        v2[0] -= m * v1[0]
        v2[1] -= m * v1[1]

    return tuple(v1), tuple(v2)

v = (846835985, 9834798552)
u = (87502093, 123094980)


reduced_v1, reduced_v2 = gauss_reduce(v, u)

inner_product = reduced_v1[0]*reduced_v2[0] + reduced_v1[1]*reduced_v2[1]

print("Reduced basis vectors:")
print("v1 =", reduced_v1)
print("v2 =", reduced_v2)
print("Inner product:", inner_product)
