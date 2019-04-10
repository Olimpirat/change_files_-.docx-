# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'close_file.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class close_file__(object):
    def setupUi(self, Dialog, x, y):
        Dialog.setObjectName("Dialog")
        Dialog.resize(x, y)
        Dialog.setMinimumSize(QtCore.QSize(200, 150))
        Dialog.setMaximumSize(QtCore.QSize(1500, 500))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_open = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_open.setFont(font)
        self.label_open.setAlignment(QtCore.Qt.AlignCenter)
        self.label_open.setObjectName("label_open")
        self.verticalLayout_2.addWidget(self.label_open)
        self.label_name_file = QtWidgets.QLabel(Dialog)
        self.label_name_file.setMinimumSize(QtCore.QSize(400, 25))
        self.label_name_file.setAlignment(QtCore.Qt.AlignCenter)
        self.label_name_file.setObjectName("label_name_file")
        self.verticalLayout_2.addWidget(self.label_name_file)
        self.label_close_file = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_close_file.setFont(font)
        self.label_close_file.setAlignment(QtCore.Qt.AlignCenter)
        self.label_close_file.setObjectName("label_close_file")
        self.verticalLayout_2.addWidget(self.label_close_file)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(100, 0, 100, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_open.setText(_translate("Dialog", "Open file:"))
        self.label_name_file.setText(_translate("Dialog", " "))
        self.label_close_file.setText(_translate("Dialog", "close this file to continue and push OK"))
        self.pushButton.setText(_translate("Dialog", "OK"))

