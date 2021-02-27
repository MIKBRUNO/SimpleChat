import socket
from MessageHandlers import data_processing as dp
import rsa
from secrets import token_bytes
from Crypto.Cipher import AES

"""
for all types of messages there are ids:
'id': 'msg'
'id': 'auth_cl'
'id': 'auth_sr'
'id': 'crypt'
'id': 'handshake'
"""


def gen_keys() -> (rsa.PublicKey, rsa.PrivateKey):
    return rsa.newkeys(500)


def prehandler(msg: dict,
               private_key: rsa.PrivateKey,
               another_key: rsa.PublicKey) -> dict:
    if msg['id'] != 'crypt':
        raise ValueError('does not encrypted!!!')
    nonce = rsa.decrypt(bytes.fromhex(msg['nonce']), private_key)
    ssk = rsa.decrypt(bytes.fromhex(msg['session_key']), private_key)
    aes_cipher = AES.new(ssk, AES.MODE_EAX, nonce=nonce)
    text = aes_cipher.decrypt(bytes.fromhex(msg['text']))
    if not rsa.verify(text, bytes.fromhex(msg['signature']), another_key):
        return {}
    else:
        text = dp.read_json(text.decode())
        return text


def cipher(msg: bytes,
           other_key: rsa.PublicKey,
           my_key: rsa.PrivateKey) -> dict:
    """
    :param msg: encoded message
    :param other_key: other's public key
    :param my_key: your side's private key
    :return: higher level of message
    :raise AssertionError:
    """
    assert other_key and my_key
    ssk = token_bytes(16)
    session_cipher = AES.new(ssk, AES.MODE_EAX)
    text = session_cipher.encrypt(msg)
    nonce = session_cipher.nonce
    nonce = rsa.encrypt(nonce, other_key)
    ssk = rsa.encrypt(ssk, other_key)
    sign = rsa.sign(msg, my_key, 'SHA-256')
    result_msg = {'text': text.hex(), 'session_key': ssk.hex(), 'nonce': nonce.hex(), 'signature': sign.hex()}
    return result_msg


def __send(sock: socket,
           msg: bytes,
           other_key: rsa.PublicKey,
           my_key: rsa.PrivateKey) -> None:
    """
    Just sends msg bytes to a socket
    standard using crypt_sys.cipher()
    :param sock: socket to send to
    :param other_key: other's public key
    :param my_key: your side's private key
    :param my_key: private client's key
    """
    res = cipher(msg, other_key, my_key)
    res['id'] = 'crypt'
    res = dp.write_json(res)
    res = res.encode()
    send(sock, res)


def send(sock: socket.socket,
         msg: bytes) -> None:
    """
    Just sends msg bytes to a socket
    standard using crypt_sys.cipher()
    :param sock: socket to send to
    :param msg: encoded message text
    """
    sock.send(msg)


def send_keys_handshake(sock: socket.socket,
                        sending_key: rsa.PublicKey) -> None:
    """
    :param sock: socket to send to
    :param sending_key: this key will be send to client (server)
    :param ftp_session_key: encrypted key to encrypt files
    """
    key = sending_key.save_pkcs1()
    msg = dp.write_json({'id': 'handshake', 'key': key.hex()})
    send(sock, msg.encode())


def make_key(key: str) -> rsa.PublicKey:
    return rsa.PublicKey.load_pkcs1(bytes.fromhex(key))


def send_chat_message_cl(sock: socket.socket,
                         sender_name: str,
                         text: str,
                         other_key: rsa.PublicKey,
                         my_key: rsa.PrivateKey) -> None:
    """
    standard is {'id': 'msg', 'sender': name, 'text': name}

    :param sock: socket that hosts SimpleChat server
    :param sender_name: client's name
    :param text: message text
    :param other_key: other's public key
    :param my_key: your side's private key
    """
    msg = dp.write_json({'id': 'msg', 'sender': sender_name, 'text': text})
    msg = msg.encode()
    __send(sock, msg, other_key, my_key)


def send_auth_request_cl(sock: socket.socket,
                         name: str,
                         password: str,
                         is_signing: bool,
                         server_password: str,
                         other_key: rsa.PublicKey,
                         my_key: rsa.PrivateKey) -> None:
    """
    standard is {'id': 'auth_cl',
                 'name': name, 'pass': password,
                 'sign': is_signing, 'srpass': server_password,
                 'email': mail_addr}
    :param sock: socket that hosts SimpleChat server
    :param name: authentication name
    :param password: password to authenticate
    :param is_signing: does user sign in SimpleChat or log in
    :param server_password: server password for more security
    :param other_key: other's public key
    :param my_key: your side's private key
    """
    msg = dp.write_json({'id': 'auth_cl',
                         'name': name,
                         'pass': password,
                         'sign': is_signing,
                         'srpass': server_password})
    msg = msg.encode()
    __send(sock, msg, other_key, my_key)


def send_auth_response_sr(sock: socket.socket,
                          auth_return: bool,
                          other_key: rsa.PublicKey,
                          my_key: rsa.PrivateKey,
                          returning_name: str = '') -> None:
    """
    standard is {'id': 'auth_sr', 'auth_return': auth_return, 'name': returning_name}
    :param sock: socket that hosts SimpleChat server
    :param auth_return: just an answer is authentication successful
    :param other_key: other's public key
    :param my_key: your side's private key
    :param returning_name: name to save if authentication successful
    """
    msg = dp.write_json({'id': 'auth_sr', 'auth_return': auth_return, 'name': returning_name})
    msg = msg.encode()
    __send(sock, msg, other_key, my_key)
