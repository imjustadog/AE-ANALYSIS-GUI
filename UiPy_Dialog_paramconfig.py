# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog_ParamConfig.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog_paramconfig(QtGui.QDialog):
    def setupUi(self, Dialog_paramconfig):
        Dialog_paramconfig.setObjectName(_fromUtf8("Dialog_paramconfig"))
        Dialog_paramconfig.resize(400, 281)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog_paramconfig)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.layoutWidget = QtGui.QWidget(Dialog_paramconfig)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 20, 287, 131))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEdit_card1_acoustic_speed = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_card1_acoustic_speed.setObjectName(_fromUtf8("lineEdit_card1_acoustic_speed"))
        self.gridLayout.addWidget(self.lineEdit_card1_acoustic_speed, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.lineEdit_card2_acoustic_speed = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_card2_acoustic_speed.setObjectName(_fromUtf8("lineEdit_card2_acoustic_speed"))
        self.gridLayout.addWidget(self.lineEdit_card2_acoustic_speed, 1, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.layoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 1, 2, 1, 1)

        self.retranslateUi(Dialog_paramconfig)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog_paramconfig.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog_paramconfig.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_paramconfig)

    def retranslateUi(self, Dialog_paramconfig):
        Dialog_paramconfig.setWindowTitle(_translate("Dialog_paramconfig", "参数配置", None))
        self.label_5.setText(_translate("Dialog_paramconfig", "m/s", None))
        self.label_3.setText(_translate("Dialog_paramconfig", "采集卡2缆索声速", None))
        self.label_2.setText(_translate("Dialog_paramconfig", "采集卡1缆索声速", None))
        self.label_6.setText(_translate("Dialog_paramconfig", "m/s", None))

