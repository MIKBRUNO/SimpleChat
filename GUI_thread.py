from PySide2.QtWidgets import (QMainWindow, QDialog)
from PySide2.QtCore import (Slot, Signal, QObject, Qt)
from Client_GUI import (Ui_MainWindow, Ui_Dialog, Ui_Register)


class MainWindow(QMainWindow):
    show_signal = Signal()
    main_closed = Signal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def closeEvent(self, event):
        self.main_closed.emit()
        event.accept()


class Dialog(QDialog):
    show_signal = Signal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # self.show_signal.connect(lambda: self.show())


class Register(QDialog):
    show_signal = Signal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_Register()
        self.ui.setupUi(self)
        # self.show_signal.connect(lambda: self.show())
