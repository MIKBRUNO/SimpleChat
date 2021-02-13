## **Message necessities**
* All messages sending must be JSON-formatted strings
* All messages must be sent by [sender.py](message_handlers.py) functions
* To add new type or add new features (like encryption and other)
you need to change [sender.py](message_handlers.py) funcs
* Handlers on server or client can process messages independently, but
it might be necessary to use special handlers to remove layers
(like using encryption)

#### **Message types**
('id' element at decrypted message dict)
* msg
* auth_cl
* auth_sr
* crypt
* handshake

#### **Message standards**
* `{'id': 'msg', 'sender': name, 'text': name}`
* `{'id': 'auth_cl', 'name': name, 'pass': password, 'sign': is_signing}`
* `{'id': 'auth_sr', 'auth_return': auth_return, 'name': returning_name}`
* `{'id': 'crypto', text': text, 'session_key': ssk, 'nonce': nonce, 'signature': sign}`
* `{'id': 'handshake', 'key': key}`
