from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import FTPHandler
import os

NAME = 'mik'
PASS = '3216547'

auth = DummyAuthorizer()
auth.add_anonymous(os.getcwd())
auth.add_user(NAME, PASS, '.')

handler = FTPHandler
handler.authorizer = auth

serv = FTPServer(('localhost', 9091), handler)
serv.serve_forever()
