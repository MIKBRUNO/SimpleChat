from MessageHandlers.message_handlers import make_key
import rsa

pk, _ = rsa.newkeys(500)
print(pk)
print(make_key(pk.save_pkcs1().hex()))
