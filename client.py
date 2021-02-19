import sys
import socket as s
from threading import Thread
from MessageHandlers.data_processing import *
from GUI.GUI import *
from PySide2.QtWidgets import (QApplication, QTextEdit, QFileDialog)
from MessageHandlers import message_handlers as mh
from ftplib import FTP
from io import BytesIO

DATA_SIZE = 1024


def handler(msg, rt):
    global reg, fail, main, server_key, password
    msg = mh.prehandler(msg, private_key, server_key)
    if msg['id'] == 'msg':
        # print(msg['sender'] + ":", msg['text'])
        main.ui.listWidget.addItem(msg['sender'] + ": " + msg['text'])
    elif msg['id'] == 'auth_sr':
        if not msg['auth_return']:
            reg.hide()
            fail.show_signal.emit()
        else:
            rt.name = msg['name']
            ftp.login(msg['name'], password)
            password = ''
            reg.hide()
            main.show_signal.emit()
            update_files_list()
    elif msg['id'] == 'handshake':
        server_key = mh.make_key(msg['key'])
        auth(reg.ui, sock)


class ReadThread(Thread):
    def __init__(self, socket):
        Thread.__init__(self)
        self.sock = socket
        self.name = ''
        self.__run = True

    def stop_thread(self):
        self.__run = False

    def run(self):
        while self.__run:
            try:
                data = self.sock.recv(DATA_SIZE)
                data = data.decode()
                message_process(data, handler, self)
            except ConnectionAbortedError:
                break


def auth(ui, socket):
    global password
    password = ui.lineEdit_2.text()
    ui.lineEdit_2.clear()
    # socket.send(write_json(
    #     {'name': ui.lineEdit.text(),
    #      'pass': password,
    #      'sign': ui.checkBox.isChecked()
    #      }).encode())
    mh.send_auth_request_cl(socket, ui.lineEdit.text(),
                            password, ui.checkBox.isChecked(),
                            server_key, private_key)


def start_connection(ui, socket, read_thread):
    if not read_thread.is_alive():
        try:
            socket.connect((ui.lineEdit_3.text(), 9090))
            ftp.connect(ui.lineEdit_3.text(), 9091)
            read_thread.start()
            mh.send_keys_handshake(socket, public_key)
        except OSError:
            global fail
            reg.hide()
            reg.ui.lineEdit_2.clear()
            fail.show_signal.emit()
            return
    else:
        auth(ui, socket)


def submit_msg(text_edit: QTextEdit):
    msg = text_edit.toPlainText()
    text_edit.clear()
    # sock.send(write_json({
    #     'sender': read_thread.name,
    #     'text': msg
    # }).encode())
    mh.send_chat_message_cl(sock, read_thread.name, msg, server_key, private_key)
    return read_thread.name + ': ' + msg


def quit_():
    read_thread.stop_thread()
    app.exit()
    sock.close()


def send_file():
    path, _ = files.getOpenFileName()
    if path != '':
        name = path.split('/')[-1]
        with open(path, 'rb') as f:
            encrypted_f_dict = mh.cipher(f.read(), server_key, private_key)
            encrypted_f_dict['id'] = 'crypt'
            encrypted_f_dict = write_json(encrypted_f_dict)
            encrypted_f_dict = encrypted_f_dict.encode()
            encrypted_f = BytesIO(encrypted_f_dict)
            ftp.storbinary('STOR ' + name, encrypted_f)
        update_files_list()


def update_files_list():
    files_list = []
    ftp.retrlines("NLST", files_list.append)
    main.ui.listWidget1.clear()
    for file in files_list:
        main.ui.listWidget1.addItem(file)


if __name__ == '__main__':
    password = ''
    sock = s.socket()
    ftp = FTP()
    read_thread = ReadThread(sock)
    app = QApplication(sys.argv)

    public_key, private_key = mh.gen_keys()
    server_key = None

    reg = Register()
    fail = Dialog()
    main = MainWindow()

    reg.ui.pushButton.clicked.connect(lambda: start_connection(reg.ui, sock, read_thread))
    reg.show_signal.connect(lambda: reg.show())
    reg.finished.connect(lambda: quit_())

    fail.show_signal.connect(lambda: fail.show())
    fail.finished.connect(lambda: reg.show())

    main.show_signal.connect(lambda: main.show())
    main.ui.pushButton.clicked.connect(lambda: main.ui.listWidget.addItem(submit_msg(main.ui.plainTextEdit)))
    main.main_closed.connect(lambda: quit_())

    files = QFileDialog()
    main.ui.pushButton_2.clicked.connect(lambda: send_file())
    main.ui.pushButton_3.clicked.connect(lambda: update_files_list())

    reg.show_signal.emit()
    sys.exit(app.exec_())
