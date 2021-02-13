from PySide2.QtWidgets import (QMainWindow, QDialog)
from PySide2.QtCore import (Signal)
from GUI.GUI_from_ui import (Ui_MainWindow, Ui_Dialog, Ui_Register)


class MainWindow(QMainWindow):
    show_signal = Signal()  # signal using to show window
    main_closed = Signal()  # signal using to run something if window closing

    def __init__(self):
        """
        connecting .ui converted to python to real widgets
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def closeEvent(self, event):
        # calls event on close window needed to close whole program
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
