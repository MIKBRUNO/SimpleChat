# https://habr.com/ru/post/205318/
import random as r
import math
import time

f_primes = [3, 5, 17, 257, 65537]
f_primes.reverse()


def check_prime(x, gcd_method=lambda a, b: euclidean_gcd(a, b)):
    if x % 2 == 0:
        return False
    for i in range(1, round(math.sqrt(x))):
        # if euclidean_gcd(i, x) != 1:
        if gcd_method(i, x) != 1:
            return False
    return True


def gen_primes2(st, fn, gcd_method=lambda a, b: euclidean_gcd(a, b)):
    a = r.randrange(st, fn)
    while not check_prime(a, gcd_method):
        a = r.randrange(st, fn)
    b = r.randrange(st, fn)
    while not check_prime(b, gcd_method) or a == b:
        b = r.randrange(st, fn)
    return a, b


def gen_keys(st: int = 1000, fn: int = 10000) -> (tuple, tuple):
    # p = 3557
    # q = 2579
    t = time.time()
    p, q = gen_primes2(st, fn, math.gcd)
    print('primes generated at {} sec'.format(time.time() - t))
    n = p * q
    fi = (p-1) * (q-1)
    # e = r.randrange(10, fi//fn)
    e = 65537
    if fi % e == 0:
        return gen_keys(st, fn)
    temp = 1
    while (temp * fi + 1) % e != 0:
        # if time.time() - t > 1:
        #     return gen_keys(st, fn)
        temp += 1
    d = (temp * fi + 1) // e
    return (e, n), (d, n)


def crypt(open_key: tuple, text: bytes):
    e = open_key[0]
    n = open_key[1]
    text = int.from_bytes(text, 'little')
    assert text < n
    c = pow(text, e, n)
    return c.to_bytes(length=c.bit_length()//8 if c.bit_length() % 8 == 0 else c.bit_length()//8 + 1,
                      byteorder='little')


def decrypt(close_key: tuple, text: bytes):
    d = close_key[0]
    n = close_key[1]
    text = int.from_bytes(text, 'little')
    c = pow(text, d, n)
    return c.to_bytes(length=c.bit_length()//8 if c.bit_length() % 8 == 0 else c.bit_length()//8 + 1,
                      byteorder='little')


def euclidean_gcd(a: int, b: int):
    """
    :doc: https://en.wikipedia.org/wiki/Euclidean_algorithm
    :param a: just a number
    :param b: number too
    :return: greatest common divisor (НОД)
    """
    if a < b:
        a, b = b, a
    if a % b == 0:
        return b
    return euclidean_gcd(b, a % b)


if __name__ == '__main__':
    t = time.time()
    print(gen_primes2(100000000000, 1000000000000, math.gcd))
    print(time.time() - t)
    t = time.time()
    print(gen_primes2(100000000000, 1000000000000, euclidean_gcd))
    print(time.time() - t)
