# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progress_bar.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_prog_bar(object):
    def setupUi(self, Dialog_prog_bar):
        Dialog_prog_bar.setObjectName("Dialog_prog_bar")
        Dialog_prog_bar.resize(300, 100)
        Dialog_prog_bar.setMinimumSize(QtCore.QSize(300, 100))
        Dialog_prog_bar.setMaximumSize(QtCore.QSize(300, 100))
        Dialog_prog_bar.setToolTip("")
        Dialog_prog_bar.setStatusTip("")
        Dialog_prog_bar.setWhatsThis("")
        self.pushButton_OK = QtWidgets.QPushButton(Dialog_prog_bar)
        self.pushButton_OK.setGeometry(QtCore.QRect(110, 60, 75, 26))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_OK.setFont(font)
        self.pushButton_OK.setObjectName("pushButton_OK")
        self.progressBar = QtWidgets.QProgressBar(Dialog_prog_bar)
        self.progressBar.setGeometry(QtCore.QRect(20, 21, 275, 25))
        self.progressBar.setMinimumSize(QtCore.QSize(275, 25))
        self.progressBar.setMaximumSize(QtCore.QSize(275, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(Dialog_prog_bar)
        QtCore.QMetaObject.connectSlotsByName(Dialog_prog_bar)

    def retranslateUi(self, Dialog_prog_bar):
        _translate = QtCore.QCoreApplication.translate
        Dialog_prog_bar.setWindowTitle(_translate("processing", "processing"))
        self.pushButton_OK.setText(_translate("Dialog_prog_bar", "OK"))

