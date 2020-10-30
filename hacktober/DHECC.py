import collections
import random

EllipticCurve = collections.namedtuple('EllipticCurve', 'name p a b g n h')

curve = EllipticCurve(
    'secp256k1',
    p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    a=0,
    b=7,
    g=(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
       0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8),
    n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
    h=1,
)


def inverse_mod(k, p):
    if k == 0:
        raise ZeroDivisionError('division by zero')

    if k < 0:
        return p - inverse_mod(-k, p)
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = p, k

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    gcd, x, y = old_r, old_s, old_t

    assert gcd == 1
    assert (k * x) % p == 1

    return x % p


def is_on_curve(point):
    if point is None:
        return True
    x, y = point[0], point[1]
    return (y * y - x * x * x - curve.a * x - curve.b) % curve.p == 0


def point_neg(point):
    assert is_on_curve(point)

    if point is None:
        return None

    x, y = point[0], point[1]
    result = (x, -y % curve.p)

    assert is_on_curve(result)

    return result


def point_add(point1, point2):
    assert is_on_curve(point1)
    assert is_on_curve(point2)

    if point1 is None:
        return point2
    if point2 is None:
        return point1

    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]

    if x1 == x2 and y1 != y2:
        return None

    if x1 == x2:
        m = (3 * x1 * x1 + curve.a) * inverse_mod(2 * y1, curve.p)
    else:
        m = (y1 - y2) * inverse_mod(x1 - x2, curve.p)

    x3 = m * m - x1 - x2
    y3 = y1 + m * (x3 - x1)
    result = (x3 % curve.p,
              -y3 % curve.p)

    assert is_on_curve(result)

    return result


def scalar_mult(k, point):
    assert is_on_curve(point)

    if k % curve.n == 0 or point is None:
        return None

    if k < 0:
        return scalar_mult(-k, point_neg(point))

    result = None
    addend = point

    while k:
        if k & 1:
            result = point_add(result, addend)

        addend = point_add(addend, addend)

        k >>= 1

    assert is_on_curve(result)

    return result


def generate_private_key():
    return random.randrange(1, curve.n)


def generate_public_key(private_key):
    return scalar_mult(private_key, curve.g)


def generate_secret(private_key, public_key):
    return scalar_mult(private_key, public_key)
'''my_private = 3296855840576710335977306677413500792974154621508589503092147326964553226041
my_public = (43221400814656949951881277786951214758909062576779005217793849373300613910542, 74871914229671147031970269069847144418734589524165582305917048541947138252141)
user_pr = 57167109010401566030779974979888395283012372853780836942954980833280897504538
x = '56836827723732971929031561626826627910735022793380491541565526966824233107728'
y = '30872013890777827469215458811801577126472533797157435190417641052987429607422'
l = []
l.append(int(x))
l.append(int(y))
user_pub = tuple(l)
print(generate_secret(my_private, user_pub))
print(generate_secret(user_pr, my_public))'''
