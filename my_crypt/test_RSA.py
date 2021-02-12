import rsa
from my_crypt.RSA import (gen_keys, crypt, decrypt)

# ok, ck = gen_keys(50000000000000, 150000000000000)

# k = rsa.PublicKey(ok[1], ok[0])

pub, priv = rsa.newkeys(128)

# print(k)
# print(pub)
# print(rsa.encrypt(b'1', k))
c = rsa.encrypt(b'1', pub)
print(c)
d = decrypt((priv.n, priv.d), c)
print(d)
