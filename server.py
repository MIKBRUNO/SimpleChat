import socket
from threading import Thread
from LOGING.Loggers import *
from MessageHandlers.data_processing import *
import bcrypt as b
from MessageHandlers import message_handlers as mh
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, TLS_FTPHandler
import os
from Crypto.Cipher import AES
from secrets import token_hex

DATA_SIZE = 1024


class FTPHostThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.__authorizer = DummyAuthorizer()
        self.__homedir = os.path.join(os.getcwd(), 'ftp\\ftp_storage')
        self.__handler = TLS_FTPHandler
        self.__handler.certfile = './.keys/cert.pem'
        self.__handler.keyfile = './.keys/key.pem'
        self.__handler.timeout = 0
        # self.__handler.ssl_protocol =
        # self.__handler = FTPHandler
        self.__handler.authorizer = self.__authorizer
        self.__server = FTPServer(('', 9091), self.__handler)

    def run(self) -> None:
        self.__server.serve_forever()

    def add_user(self, name: str, password: str):
        if not self.__server.handler.authorizer.has_user(name):
            self.__server.handler.authorizer.add_user(name, password, self.__homedir, 'wrl')


class ConnectorThread(Thread):
    def __init__(self, input_socket):
        Thread.__init__(self)
        self.sock = input_socket
        self.conns = []
        with open('users.json', 'r') as js:
            self.users = read_json(js.read())

    def connection_closes(self, connection, name):
        self.conns.remove(connection)
        write_to_main_log('EVENT', name + ' disconnected')
        connection.connection.close()
        write_to_main_log('Connector', self.conns.__str__())

    def run(self):
        while True:
            conn, adr = self.sock.accept()
            rt = ReadThread(conn, self)
            rt.start()
            self.conns.append(rt)
            write_to_main_log('Connector', self.conns.__str__())


class ReadThread(Thread):
    def __init__(self, connection, parental_connector):
        Thread.__init__(self)
        self.connection = connection
        self.parent = parental_connector
        self.name = 'not registered'
        self.registered = False
        self.client_key = None
        self.ftp_key: AES = None

    def run(self):
        while True:
            try:
                data = self.connection.recv(DATA_SIZE)
                if not self.data_process(data):
                    self.parent.connection_closes(self, self.name)
                    break
            except ConnectionResetError:
                self.parent.connection_closes(self, self.name)
                break

    def data_process(self, data):
        data_ = data.decode()
        if not data_:
            return False
        else:
            message_process(data_, handler, self)
            return True


def write_users(users):
    with open('users.json', 'w') as js:
        js.write(write_json(users))


def handler(msg_dict, rt: ReadThread):
    if msg_dict['id'] == 'handshake':
        rt.client_key = mh.make_key(msg_dict['key'])
        mh.send_keys_handshake(rt.connection, public_key)
        write_to_main_log('Crypto', 'handshake done')
    else:
        try:
            msg_dict = mh.prehandler(msg_dict, private_key, rt.client_key)
        except ValueError:
            return
        if msg_dict['id'] == 'msg':
            for conn in rt.parent.conns:
                if conn != rt and conn.registered:
                    mh.send_chat_message_cl(conn.connection, msg_dict['sender'], msg_dict['text'], conn.client_key,
                                            private_key)
        elif msg_dict['id'] == 'auth_cl':
            authenticate(msg_dict, rt)


def authenticate(msg_dict, rt):
    ct = rt.parent
    conn = rt.connection
    if msg_dict['sign']:
        if msg_dict['srpass'] != host_password:
            mh.send_auth_response_sr(conn, False, rt.client_key, private_key, '')
        elif msg_dict['name'] in [name for name in ct.users]:
            # conn.send(write_json({'auth_return': False}).encode())
            mh.send_auth_response_sr(conn, False, rt.client_key, private_key, '')
        else:
            salt = b.gensalt()
            ciphered = b.hashpw(msg_dict['pass'].encode(), salt)
            ct.users[msg_dict['name']] = ciphered.decode()
            write_users(ct.users)
            rt.registered = True
            rt.name = msg_dict['name']
            write_to_main_log('EVENT', msg_dict['name'] + ' connected')
            # conn.send(write_json({'auth_return': True, 'name': msg_dict['name']}).encode())
            mh.send_auth_response_sr(conn, True, rt.client_key, private_key, msg_dict['name'])
            write_to_main_log('EVENT', msg_dict['name'] + ' connected')
            ftp_thread.add_user(msg_dict['name'], msg_dict['pass'])
    else:
        if msg_dict['srpass'] != host_password:
            mh.send_auth_response_sr(conn, False, rt.client_key, private_key, '')
        elif not ct.users or \
                msg_dict['name'] not in ct.users or \
                not b.checkpw(msg_dict['pass'].encode(), ct.users[msg_dict['name']].encode()) or\
                msg_dict['name'] in [i.name for i in ct.conns]:
            # conn.send(write_json({'auth_return': False}).encode())
            mh.send_auth_response_sr(conn, False, rt.client_key, private_key, '')
        else:
            rt.name = msg_dict['name']
            rt.registered = True
            # conn.send(write_json({'auth_return': True, 'name': msg_dict['name']}).encode())
            mh.send_auth_response_sr(conn, True, rt.client_key, private_key, msg_dict['name'])
            write_to_main_log('EVENT', msg_dict['name'] + ' connected')
            ftp_thread.add_user(msg_dict['name'], msg_dict['pass'])


if __name__ == '__main__':
    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen()

    public_key, private_key = mh.gen_keys()

    host_password = token_hex(3)
    print(host_password)

    connector = ConnectorThread(sock)
    connector.start()

    ftp_thread = FTPHostThread()
    ftp_thread.start()
