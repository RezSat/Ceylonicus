# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from main import Execute
import os

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(737, 568)
        font = QtGui.QFont()
        font.setFamily("Iskoola Pota")
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        MainWindow.setFont(font)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Iskoola Pota")
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")

        self.run = QtWidgets.QPushButton(self.centralwidget)
        self.run.setGeometry(QtCore.QRect(20, 450, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Iskoola Pota")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.run.setFont(font)
        self.run.setObjectName("run")
        self.run.clicked.connect(self.code_run)

        self.font_size_increaser = QtWidgets.QSlider(self.centralwidget)
        self.font_size_increaser.setGeometry(QtCore.QRect(250, 460, 221, 19))
        font = QtGui.QFont()
        font.setFamily("Iskoola Pota")
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.font_size_increaser.setFont(font)
        self.font_size_increaser.setOrientation(QtCore.Qt.Horizontal)
        self.font_size_increaser.setObjectName("font_size_increaser")
        self.font_size_increaser.valueChanged.connect(self.font_sizer)

        self.font_size = QtWidgets.QLabel(self.centralwidget)
        self.font_size.setGeometry(QtCore.QRect(340, 440, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Iskoola Pota")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.font_size.setFont(font)
        self.font_size.setObjectName("font_size")

        self.code_input = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.code_input.setGeometry(QtCore.QRect(10, 10, 461, 421))
        font = QtGui.QFont()
        font.setFamily("Iskoola Pota")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.code_input.setFont(font)
        self.code_input.setObjectName("code_input")

        self.result = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.result.setGeometry(QtCore.QRect(490, 10, 231, 421))
        font = QtGui.QFont()
        font.setFamily("Iskoola Pota")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.result.setFont(font)
        self.result.setObjectName("result")

        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Iskoola Pota")
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.statusbar.setFont(font)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.run.setText(_translate("MainWindow", "RUN"))
        self.font_size.setText(_translate("MainWindow", "Font Size"))

    def code_run(self):
        _printed_ = open('_printed_','w')
        _printed_.close()
        text = self.code_input.document().toPlainText()
        with open('somefile', 'w', encoding='utf-8') as f:
            f.write(text)
            f.close()
        os.system('py shell.py')
        _printed_ = open('_printed_','r',encoding='utf-8').read()
        self.result.setPlainText(_printed_.encode("utf8").decode(sys.stdout.encoding))

    def font_sizer(self):
        size = self.font_size_increaser.value()
        if int(size) == 0:
            size = 1
        self.font_size.setText(f"Font size: {size}")
        font = QtGui.QFont()
        font.setFamily("Iskoola Pota")
        font.setPointSize(size)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.code_input.setFont(font)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())