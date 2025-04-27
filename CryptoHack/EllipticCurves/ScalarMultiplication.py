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
        return None

    if P != Q:
        m = (y2 - y1) * inverse_mod(x2 - x1, p) % p
    else:
        m = (3 * x1 * x1 + a) * inverse_mod(2 * y1, p) % p

    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p

    return (x3, y3)


def scalar_mult(k, P, a, p):
   
    R = None  
    Q = P

    while k > 0:
        if k % 2 == 1:
            R = point_add(R, Q, a, p)
        Q = point_add(Q, Q, a, p)
        k //= 2

    return R


# Curve parameters
p = 9739
a = 497

# Given point and scalar
P = (2339, 2213)
n = 7863

# Calculate Q = [n]P
Q = scalar_mult(n, P, a, p)

print(f"The final point Q is: {Q}")


if Q is not None:
    x, y = Q
    is_on_curve = (y * y - (x * x * x + a * x + 1768)) % p == 0
    print(f"Is Q on the curve? {is_on_curve}")
