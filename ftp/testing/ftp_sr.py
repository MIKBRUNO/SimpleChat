from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import FTPHandler
import os

NAME = 'mik'
PASS = '3216547'

auth = DummyAuthorizer()
auth.add_anonymous(os.getcwd())
auth.add_user(NAME, PASS, os.path.join(os.getcwd(), '..\\ftp_base'), auth.write_perms+auth.read_perms)
# auth.add_user(NAME, PASS, os.path.join(os.getcwd(), '..\\ftp_base'))
print(os.path.join(os.getcwd(), '..\\ftp_base'))

handler = FTPHandler
handler.authorizer = auth

serv = FTPServer(('localhost', 9091), handler)
serv.serve_forever()
