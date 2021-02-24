from secrets import token_bytes
from Crypto.Cipher import AES

key = token_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)
print(key)
print(cipher.nonce)
