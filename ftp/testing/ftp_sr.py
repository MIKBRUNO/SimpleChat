from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import FTPHandler
import os
from threading import Thread

NAME = 'mik'
PASS = '3216547'

auth = DummyAuthorizer()
# auth.add_anonymous(os.getcwd())

handler = FTPHandler
handler.authorizer = auth

serv = FTPServer(('localhost', 9091), handler)

thread = Thread()
thread.run = lambda: serv.serve_forever()

thread.start()

auth.add_user(NAME, PASS, os.path.join(os.getcwd(), '..\\ftp_storage'), 'wr')
