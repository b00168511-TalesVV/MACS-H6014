def inverse_mod(k, p):
   
    if k == 0:
        raise ZeroDivisionError('division by zero')
    return pow(k, -1, p)  


def point_add(P, Q, a, p):
    
    if P is None:
        return Q
    if Q is None:
        return P

    (x1, y1) = P
    (x2, y2) = Q

    if x1 == x2 and (y1 != y2 or y1 == 0):
        # P + (-P) = O
        return None

    if P != Q:
        # lambda = (y2 - y1) / (x2 - x1)
        m = (y2 - y1) * inverse_mod(x2 - x1, p) % p
    else:
        # Point doubling: lambda = (3 * x1^2 + a) / (2 * y1)
        m = (3 * x1 * x1 + a) * inverse_mod(2 * y1, p) % p

    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p

    return (x3, y3)


p = 9739
a = 497

P = (493, 5564)
Q = (1539, 4742)
R = (4403, 5202)


P2 = point_add(P, P, a, p)

P2_Q = point_add(P2, Q, a, p)


S = point_add(P2_Q, R, a, p)

print(f"The final point S is: {S}")


if S is not None:
    x, y = S
    is_on_curve = (y * y - (x * x * x + a * x + 1768)) % p == 0
    print(f"Is S on the curve? {is_on_curve}")
