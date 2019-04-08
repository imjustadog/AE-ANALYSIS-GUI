# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog_Calibration.ui'
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

class Ui_Dialog_calibration(QtGui.QDialog):
    def setupUi(self, Dialog_calibration):
        Dialog_calibration.setObjectName(_fromUtf8("Dialog_calibration"))
        Dialog_calibration.resize(417, 654)
        self.comboBox_choose_card = QtGui.QComboBox(Dialog_calibration)
        self.comboBox_choose_card.setGeometry(QtCore.QRect(110, 30, 91, 27))
        self.comboBox_choose_card.setObjectName(_fromUtf8("comboBox_choose_card"))
        self.comboBox_choose_card.addItem(_fromUtf8(""))
        self.comboBox_choose_card.addItem(_fromUtf8(""))
        self.label_4 = QtGui.QLabel(Dialog_calibration)
        self.label_4.setGeometry(QtCore.QRect(10, 80, 91, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.lineEdit_sensor2_location = QtGui.QLineEdit(Dialog_calibration)
        self.lineEdit_sensor2_location.setGeometry(QtCore.QRect(110, 130, 113, 27))
        self.lineEdit_sensor2_location.setObjectName(_fromUtf8("lineEdit_sensor2_location"))
        self.label_5 = QtGui.QLabel(Dialog_calibration)
        self.label_5.setGeometry(QtCore.QRect(10, 130, 91, 17))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(Dialog_calibration)
        self.label_6.setGeometry(QtCore.QRect(10, 30, 91, 17))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.lineEdit_sensor1_location = QtGui.QLineEdit(Dialog_calibration)
        self.lineEdit_sensor1_location.setGeometry(QtCore.QRect(110, 80, 113, 27))
        self.lineEdit_sensor1_location.setObjectName(_fromUtf8("lineEdit_sensor1_location"))
        self.label_7 = QtGui.QLabel(Dialog_calibration)
        self.label_7.setGeometry(QtCore.QRect(10, 180, 91, 17))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.lineEdit_source_location = QtGui.QLineEdit(Dialog_calibration)
        self.lineEdit_source_location.setGeometry(QtCore.QRect(110, 180, 113, 27))
        self.lineEdit_source_location.setObjectName(_fromUtf8("lineEdit_source_location"))
        self.label_capture_count = QtGui.QLabel(Dialog_calibration)
        self.label_capture_count.setGeometry(QtCore.QRect(100, 240, 141, 17))
        self.label_capture_count.setObjectName(_fromUtf8("label_capture_count"))
        self.label_10 = QtGui.QLabel(Dialog_calibration)
        self.label_10.setGeometry(QtCore.QRect(10, 280, 81, 17))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(Dialog_calibration)
        self.label_11.setGeometry(QtCore.QRect(230, 180, 21, 17))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_12 = QtGui.QLabel(Dialog_calibration)
        self.label_12.setGeometry(QtCore.QRect(230, 130, 21, 17))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_13 = QtGui.QLabel(Dialog_calibration)
        self.label_13.setGeometry(QtCore.QRect(230, 80, 21, 17))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.label = QtGui.QLabel(Dialog_calibration)
        self.label.setGeometry(QtCore.QRect(10, 570, 68, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit_best_frequency = QtGui.QLineEdit(Dialog_calibration)
        self.lineEdit_best_frequency.setGeometry(QtCore.QRect(80, 570, 113, 27))
        self.lineEdit_best_frequency.setObjectName(_fromUtf8("lineEdit_best_frequency"))
        self.lineEdit_acoustic_speed = QtGui.QLineEdit(Dialog_calibration)
        self.lineEdit_acoustic_speed.setGeometry(QtCore.QRect(80, 620, 113, 27))
        self.lineEdit_acoustic_speed.setObjectName(_fromUtf8("lineEdit_acoustic_speed"))
        self.label_2 = QtGui.QLabel(Dialog_calibration)
        self.label_2.setGeometry(QtCore.QRect(10, 620, 68, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_15 = QtGui.QLabel(Dialog_calibration)
        self.label_15.setGeometry(QtCore.QRect(200, 570, 21, 17))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.label_16 = QtGui.QLabel(Dialog_calibration)
        self.label_16.setGeometry(QtCore.QRect(200, 620, 41, 17))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.pushButton_calculate = QtGui.QPushButton(Dialog_calibration)
        self.pushButton_calculate.setGeometry(QtCore.QRect(10, 520, 81, 27))
        self.pushButton_calculate.setObjectName(_fromUtf8("pushButton_calculate"))
        self.pushButton_change_location = QtGui.QPushButton(Dialog_calibration)
        self.pushButton_change_location.setGeometry(QtCore.QRect(260, 180, 61, 27))
        self.pushButton_change_location.setObjectName(_fromUtf8("pushButton_change_location"))
        self.pushButton_start_to_capture = QtGui.QPushButton(Dialog_calibration)
        self.pushButton_start_to_capture.setGeometry(QtCore.QRect(10, 230, 81, 27))
        self.pushButton_start_to_capture.setObjectName(_fromUtf8("pushButton_start_to_capture"))
        self.textEdit_time_difference = QtGui.QTextEdit(Dialog_calibration)
        self.textEdit_time_difference.setGeometry(QtCore.QRect(70, 280, 231, 171))
        self.textEdit_time_difference.setObjectName(_fromUtf8("textEdit_time_difference"))
        self.lineEdit_path = QtGui.QLineEdit(Dialog_calibration)
        self.lineEdit_path.setEnabled(False)
        self.lineEdit_path.setGeometry(QtCore.QRect(130, 470, 151, 27))
        self.lineEdit_path.setObjectName(_fromUtf8("lineEdit_path"))
        self.pushButton_choose_path = QtGui.QPushButton(Dialog_calibration)
        self.pushButton_choose_path.setEnabled(False)
        self.pushButton_choose_path.setGeometry(QtCore.QRect(280, 470, 21, 27))
        self.pushButton_choose_path.setObjectName(_fromUtf8("pushButton_choose_path"))
        self.checkBox_choose_path = QtGui.QCheckBox(Dialog_calibration)
        self.checkBox_choose_path.setGeometry(QtCore.QRect(10, 470, 121, 22))
        self.checkBox_choose_path.setObjectName(_fromUtf8("checkBox_choose_path"))
        self.pushButton_stop_to_capture = QtGui.QPushButton(Dialog_calibration)
        self.pushButton_stop_to_capture.setGeometry(QtCore.QRect(260, 230, 81, 27))
        self.pushButton_stop_to_capture.setObjectName(_fromUtf8("pushButton_stop_to_capture"))

        self.retranslateUi(Dialog_calibration)
        QtCore.QMetaObject.connectSlotsByName(Dialog_calibration)

    def retranslateUi(self, Dialog_calibration):
        Dialog_calibration.setWindowTitle(_translate("Dialog_calibration", "calibration", None))
        self.comboBox_choose_card.setItemText(0, _translate("Dialog_calibration", "采集卡1", None))
        self.comboBox_choose_card.setItemText(1, _translate("Dialog_calibration", "采集卡2", None))
        self.label_4.setText(_translate("Dialog_calibration", "传感器1位置", None))
        self.label_5.setText(_translate("Dialog_calibration", "传感器2位置", None))
        self.label_6.setText(_translate("Dialog_calibration", "采集卡编号", None))
        self.label_7.setText(_translate("Dialog_calibration", "声发射源位置", None))
        self.label_capture_count.setText(_translate("Dialog_calibration", "正在进行第0次采集", None))
        self.label_10.setText(_translate("Dialog_calibration", "时间差", None))
        self.label_11.setText(_translate("Dialog_calibration", "m", None))
        self.label_12.setText(_translate("Dialog_calibration", "m", None))
        self.label_13.setText(_translate("Dialog_calibration", "m", None))
        self.label.setText(_translate("Dialog_calibration", "最佳频率", None))
        self.label_2.setText(_translate("Dialog_calibration", "声速", None))
        self.label_15.setText(_translate("Dialog_calibration", "Hz", None))
        self.label_16.setText(_translate("Dialog_calibration", "m/s", None))
        self.pushButton_calculate.setText(_translate("Dialog_calibration", "标定", None))
        self.pushButton_change_location.setText(_translate("Dialog_calibration", "修改", None))
        self.pushButton_start_to_capture.setText(_translate("Dialog_calibration", "采集开始", None))
        self.pushButton_choose_path.setText(_translate("Dialog_calibration", "...", None))
        self.checkBox_choose_path.setText(_translate("Dialog_calibration", "自由选取样本", None))
        self.pushButton_stop_to_capture.setText(_translate("Dialog_calibration", "停止采集", None))

