from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


"""
.ui converted to python
to convert:
PySide2-uic GUI.ui 
or
PySide2-uic GUI.ui >> PyGUI.ui 
"""


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(232, 118)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 30, 231, 51))
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"SimpleChat", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Failed", None))
    # retranslateUi

class Ui_Register(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(362, 245)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(270, 150, 75, 23))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 70, 80, 13))
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 110, 100, 13))
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(120, 70, 230, 20))
        self.lineEdit_2 = QLineEdit(Dialog)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(120, 110, 230, 20))
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(60, 30, 47, 13))
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lineEdit_3 = QLineEdit(Dialog)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(120, 30, 230, 20))
        self.checkBox = QCheckBox(Dialog)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(190, 150, 70, 17))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"SimpleChat", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Connect", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Enter ur name", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Enter ur password", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Address", None))
        self.checkBox.setText(QCoreApplication.translate("Dialog", u"Sign In", None))
    # retranslateUi

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(622, 546)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.actionLog_In = QAction(MainWindow)
        self.actionLog_In.setObjectName(u"actionLog_In")
        self.actionSign_In = QAction(MainWindow)
        self.actionSign_In.setObjectName(u"actionSign_In")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(10, 10, 320, 440))
        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(10, 460, 231, 51))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(250, 470, 71, 31))
        self.pushButton.setAutoDefault(True)
        self.listWidget1 = QListWidget(self.centralwidget)
        self.listWidget1.setObjectName(u"listWidget1")
        self.listWidget1.setGeometry(QRect(341, 10, 275, 440))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(350, 460, 90, 50))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(450, 470, 60, 30))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(520, 470, 75, 30))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 622, 21))
        self.menuhello = QMenu(self.menuBar)
        self.menuhello.setObjectName(u"menuhello")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuhello.menuAction())
        self.menuhello.addAction(self.actionLog_In)
        self.menuhello.addAction(self.actionSign_In)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SimpleChat", None))
        self.actionLog_In.setText(QCoreApplication.translate("MainWindow", u"Log In", None))
        self.actionSign_In.setText(QCoreApplication.translate("MainWindow", u"Sign In", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Submit", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Select file", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Chose", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Update List", None))
        self.menuhello.setTitle(QCoreApplication.translate("MainWindow", u"Connect", None))
    # retranslateUi
