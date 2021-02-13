import socket
from threading import Thread
from Testing.Loggers import *
from DataProcessing import *
import bcrypt as b
import sender as send

DATA_SIZE = 1024


def write_users(users):
    with open('users.json', 'w') as js:
        js.write(write_json(users))


def handler(msg_dict, rt):
    if msg_dict['id'] == 'msg':
        for conn in rt.parent.conns:
            if conn != rt and conn.registered:
                conn.connection.send(write_json(msg_dict).encode())
    elif msg_dict['id'] == 'auth_cl':
        authenticate(msg_dict, rt)


def authenticate(msg_dict, rt):
    ct = rt.parent
    conn = rt.connection
    if msg_dict['sign']:
        if msg_dict['name'] in [name for name in ct.users]:
            # conn.send(write_json({'auth_return': False}).encode())
            send.send_auth_response_sr(conn, False)
        else:
            salt = b.gensalt()
            ciphered = b.hashpw(msg_dict['pass'].encode(), salt)
            ct.users[msg_dict['name']] = ciphered.decode()
            write_users(ct.users)
            rt.registered = True
            rt.name = msg_dict['name']
            write_to_main_log('EVENT', msg_dict['name'] + ' connected')
            # conn.send(write_json({'auth_return': True, 'name': msg_dict['name']}).encode())
            send.send_auth_response_sr(conn, True, msg_dict['name'])
    else:
        if not ct.users or \
                msg_dict['name'] not in ct.users or \
                not b.checkpw(msg_dict['pass'].encode(), ct.users[msg_dict['name']].encode()):
            # conn.send(write_json({'auth_return': False}).encode())
            send.send_auth_response_sr(conn, False)
        else:
            rt.name = msg_dict['name']
            rt.registered = True
            # conn.send(write_json({'auth_return': True, 'name': msg_dict['name']}).encode())
            send.send_auth_response_sr(conn, True, msg_dict['name'])
            write_to_main_log('EVENT', msg_dict['name'] + ' connected')


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

    def run(self):
        while True:
            conn, adr = self.sock.accept()
            rt = ReadThread(conn, self)
            rt.start()
            self.conns.append(rt)


class ReadThread(Thread):
    def __init__(self, connection, parental_connector):
        Thread.__init__(self)
        self.connection = connection
        self.parent = parental_connector
        self.name = 'not registered'
        self.registered = False

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


if __name__ == '__main__':
    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen()

    connector = ConnectorThread(sock)
    connector.start()
