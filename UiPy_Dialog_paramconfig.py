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
        self.layoutWidget.setGeometry(QtCore.QRect(30, 20, 287, 198))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_sensor1loc = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_sensor1loc.setObjectName(_fromUtf8("lineEdit_sensor1loc"))
        self.gridLayout.addWidget(self.lineEdit_sensor1loc, 1, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit_cablelength = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_cablelength.setObjectName(_fromUtf8("lineEdit_cablelength"))
        self.gridLayout.addWidget(self.lineEdit_cablelength, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_sensor2loc = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_sensor2loc.setObjectName(_fromUtf8("lineEdit_sensor2loc"))
        self.gridLayout.addWidget(self.lineEdit_sensor2loc, 2, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.layoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 2, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)
        self.label_7 = QtGui.QLabel(self.layoutWidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)
        self.lineEdit_speedcompensate = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_speedcompensate.setObjectName(_fromUtf8("lineEdit_speedcompensate"))
        self.gridLayout.addWidget(self.lineEdit_speedcompensate, 5, 1, 1, 1)
        self.checkBox_sensor2enabled = QtGui.QCheckBox(self.layoutWidget)
        self.checkBox_sensor2enabled.setObjectName(_fromUtf8("checkBox_sensor2enabled"))
        self.gridLayout.addWidget(self.checkBox_sensor2enabled, 2, 3, 1, 1)
        self.checkBox_sensor1enabled = QtGui.QCheckBox(self.layoutWidget)
        self.checkBox_sensor1enabled.setObjectName(_fromUtf8("checkBox_sensor1enabled"))
        self.gridLayout.addWidget(self.checkBox_sensor1enabled, 1, 3, 1, 1)
        self.lineEdit_sensor3loc = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_sensor3loc.setObjectName(_fromUtf8("lineEdit_sensor3loc"))
        self.gridLayout.addWidget(self.lineEdit_sensor3loc, 3, 1, 1, 1)
        self.lineEdit_sensor4loc = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_sensor4loc.setObjectName(_fromUtf8("lineEdit_sensor4loc"))
        self.gridLayout.addWidget(self.lineEdit_sensor4loc, 4, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.layoutWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1)
        self.label_9 = QtGui.QLabel(self.layoutWidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 4, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.layoutWidget)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 3, 2, 1, 1)
        self.label_11 = QtGui.QLabel(self.layoutWidget)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 4, 2, 1, 1)
        self.checkBox_sensor3enabled = QtGui.QCheckBox(self.layoutWidget)
        self.checkBox_sensor3enabled.setObjectName(_fromUtf8("checkBox_sensor3enabled"))
        self.gridLayout.addWidget(self.checkBox_sensor3enabled, 3, 3, 1, 1)
        self.checkBox_sensor4enabled = QtGui.QCheckBox(self.layoutWidget)
        self.checkBox_sensor4enabled.setObjectName(_fromUtf8("checkBox_sensor4enabled"))
        self.gridLayout.addWidget(self.checkBox_sensor4enabled, 4, 3, 1, 1)

        self.retranslateUi(Dialog_paramconfig)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog_paramconfig.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog_paramconfig.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_paramconfig)

    def retranslateUi(self, Dialog_paramconfig):
        Dialog_paramconfig.setWindowTitle(_translate("Dialog_paramconfig", "参数配置", None))
        self.label.setText(_translate("Dialog_paramconfig", "缆索总长", None))
        self.label_5.setText(_translate("Dialog_paramconfig", "cm", None))
        self.label_3.setText(_translate("Dialog_paramconfig", "传感器2位置", None))
        self.label_2.setText(_translate("Dialog_paramconfig", "传感器1位置", None))
        self.label_6.setText(_translate("Dialog_paramconfig", "cm", None))
        self.label_4.setText(_translate("Dialog_paramconfig", "cm", None))
        self.label_7.setText(_translate("Dialog_paramconfig", "声速补偿系数", None))
        self.checkBox_sensor2enabled.setText(_translate("Dialog_paramconfig", "使能", None))
        self.checkBox_sensor1enabled.setText(_translate("Dialog_paramconfig", "使能", None))
        self.label_8.setText(_translate("Dialog_paramconfig", "传感器3位置", None))
        self.label_9.setText(_translate("Dialog_paramconfig", "传感器4位置", None))
        self.label_10.setText(_translate("Dialog_paramconfig", "cm", None))
        self.label_11.setText(_translate("Dialog_paramconfig", "cm", None))
        self.checkBox_sensor3enabled.setText(_translate("Dialog_paramconfig", "使能", None))
        self.checkBox_sensor4enabled.setText(_translate("Dialog_paramconfig", "使能", None))

