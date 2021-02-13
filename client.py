import sys
import socket as s
from threading import Thread
from DataProcessing import *
from GUI_thread import *
from PySide2.QtWidgets import (QApplication, QTextEdit)
import sender as send
import crypt_sys as cs

DATA_SIZE = 1024


def handler(msg, rt):
    global reg, fail, main
    if msg['id'] == 'msg':
        # print(msg['sender'] + ":", msg['text'])
        main.ui.listWidget.addItem(msg['sender'] + ": " + msg['text'])
    elif msg['id'] == 'auth_sr':
        if not msg['auth_return']:
            reg.hide()
            fail.show_signal.emit()
        else:
            rt.name = msg['name']
            reg.hide()
            main.show_signal.emit()


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


def auth(ui, socket, read_thread):
    try:
        socket.connect((ui.lineEdit_3.text(), 9090))
        read_thread.start()
    except OSError:
        global fail
        reg.hide()
        reg.ui.lineEdit_2.clear()
        fail.show_signal.emit()
        return
    password = ui.lineEdit_2.text()
    ui.lineEdit_2.clear()
    # socket.send(write_json(
    #     {'name': ui.lineEdit.text(),
    #      'pass': password,
    #      'sign': ui.checkBox.isChecked()
    #      }).encode())
    send.send_auth_request_cl(socket, ui.lineEdit.text(),
                              password, ui.checkBox.isChecked())


def submit_msg(text_edit: QTextEdit):
    msg = text_edit.toPlainText()
    text_edit.clear()
    # sock.send(write_json({
    #     'sender': read_thread.name,
    #     'text': msg
    # }).encode())
    send.send_chat_message_cl(sock, read_thread.name, msg)
    return read_thread.name + ': ' + msg


def quit_():
    read_thread.stop_thread()
    app.exit()
    sock.close()


if __name__ == '__main__':
    sock = s.socket()
    public_key, private_key = cs.gen_rsa_keys()
    read_thread = ReadThread(sock)
    app = QApplication(sys.argv)

    reg = Register()
    fail = Dialog()
    main = MainWindow()

    reg.ui.pushButton.clicked.connect(lambda: auth(reg.ui, sock, read_thread))
    reg.show_signal.connect(lambda: reg.show())

    fail.show_signal.connect(lambda: fail.show())
    fail.finished.connect(lambda: reg.show())

    main.show_signal.connect(lambda: main.show())
    main.ui.pushButton.clicked.connect(lambda: main.ui.listWidget.addItem(submit_msg(main.ui.plainTextEdit)))
    main.main_closed.connect(lambda: quit_())

    reg.show_signal.emit()
    sys.exit(app.exec_())
