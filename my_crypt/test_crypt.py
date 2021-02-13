# https://habr.com/ru/post/212235/
from Crypto.Cipher import AES
from secrets import token_bytes
import rsa
import DataProcessing as dp

message = 'super secret Alice\'s message'
name = 'Alice'

# Alice gen keys for signature
a_pk, a_sk = rsa.newkeys(500)

# Bob gen keys
public_key, private_key = rsa.newkeys(500)

# Alice digital signature
msg = dp.write_json({'text': message, 'name': name})
# salt = bcrypt.gensalt()
print('encoded msg:', msg.encode())
# msg_hash = bcrypt.hashpw(msg.encode(), salt)
# dig_sign = rsa.encrypt(msg_hash, a_sk)
dig_sign = rsa.sign(msg.encode(), a_sk, 'SHA-256')

# Alice message crypt
symmetric_key = token_bytes(16)
print('symmetric_key:', symmetric_key)
cipher = AES.new(symmetric_key, AES.MODE_EAX)
encrypted = cipher.encrypt(msg.encode())

# Alice cipher symmetric key
sym_key_encrypted = rsa.encrypt(symmetric_key, public_key)

# Alice sends
ALICE_MSG = {'text': encrypted.hex(), 'dig_sign': dig_sign.hex(),
             'sym_key': sym_key_encrypted.hex(), 'nonce': rsa.encrypt(cipher.nonce, public_key).hex()}
print(ALICE_MSG)

# Bob gets
del message, name, msg,\
    dig_sign, symmetric_key, sym_key_encrypted,\
    cipher, encrypted

text = ALICE_MSG['text']
dig_sign = ALICE_MSG['dig_sign']
sym_key = ALICE_MSG['sym_key']
nonce = ALICE_MSG['nonce']

# Bob decrypts
sym_key = bytes.fromhex(sym_key)
sym_key = rsa.decrypt(sym_key, private_key)
print('symmetric_key', sym_key)

text = bytes.fromhex(text)
cipher = AES.new(sym_key, AES.MODE_EAX, nonce=rsa.decrypt(bytes.fromhex(nonce), private_key))
text = cipher.decrypt(text)
print('encoded msg:', text)
text = text.decode()
dig_sign = bytes.fromhex(dig_sign)
corrupted = not rsa.verify(text.encode(), dig_sign, a_pk)
print('message {} corrupted'.format('not' if not corrupted else ''))
