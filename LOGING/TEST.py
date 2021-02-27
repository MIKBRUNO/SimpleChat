from threading import Thread
from socket import socket
import rsa
import json
from MessageHandlers.message_handlers import cipher, send_chat_message_cl, gen_keys
import time

sock = socket()
sock.connect(('localhost', 9090))


class listenThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.ret = None

    def run(self):
        while not self.ret:
            self.ret = sock.recv(1024)


pk, sk = gen_keys()
pk_ = pk.save_pkcs1().hex()
handshake = {'id': 'handshake', 'key': pk_}

lt = listenThread()
lt.start()

sock.send(json.dumps(handshake).encode())
time.sleep(2)

serv = lt.ret
serv = rsa.PublicKey.load_pkcs1()

cr = cipher(json.dumps(msg).encode(), serv_key, sk)
cr['id'] = 'crypto'

# sock.send(json.dumps(cr).encode())
send_chat_message_cl(sock, 'Mallory', 'corrupted', serv_key, sk)
