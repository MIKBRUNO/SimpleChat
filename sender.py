import socket
import DataProcessing as dtprc
import crypt_sys


"""
for all types of messages there are ids:
'id': 'msg';
'id': 'auth_cl';
'id': 'auth_sr'
"""


def __send(sock: socket,
           msg: bytes) -> None:
    sock.send(msg)


def send_chat_message_cl(sock: socket.socket,
                      sender_name: str,
                      text: str) -> None:
    """
    standard is {'id': 'msg', 'sender': name, 'text': name}

    :param sock: socket that hosts SimpleChat server
    :param sender_name: client's name
    :param text: message text
    """
    msg = dtprc.write_json({'id': 'msg', 'sender': sender_name, 'text': text})
    msg = msg.encode()
    __send(sock, msg)


def send_auth_request_cl(sock: socket.socket,
                         name: str,
                         password: str,
                         is_signing: bool) -> None:
    msg = dtprc.write_json({'id': 'auth_cl', 'name': name, 'pass': password, 'sign': is_signing})
    msg = msg.encode()
    __send(sock, msg)


def send_auth_response_sr(sock: socket.socket,
                          auth_return: bool,
                          returning_name: str = '') -> None:
    msg = dtprc.write_json({'id': 'auth_sr', 'auth_return': auth_return, 'name': returning_name})
    msg = msg.encode()
    __send(sock, msg)
