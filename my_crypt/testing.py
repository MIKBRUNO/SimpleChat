import secrets
from Crypto.Cipher import AES

key = secrets.token_bytes(16)

cipher = AES.new(key, AES.MODE_EAX)

e, dig = cipher.encrypt_and_digest(b'some text')

cipher = AES.new(key, AES.MODE_EAX, nonce=cipher.nonce)
print(cipher.verify(dig))

print(e, dig)
