# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog_Showfitting.ui'
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

class Ui_Dialog_showfitting(QtGui.QDialog):
    def setupUi(self, Dialog_showfitting):
        Dialog_showfitting.setObjectName(_fromUtf8("Dialog_showfitting"))
        Dialog_showfitting.resize(712, 496)
        self.gridLayout = QtGui.QGridLayout(Dialog_showfitting)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.widget = PlotWidget(Dialog_showfitting)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        self.retranslateUi(Dialog_showfitting)
        QtCore.QMetaObject.connectSlotsByName(Dialog_showfitting)

    def retranslateUi(self, Dialog_showfitting):
        Dialog_showfitting.setWindowTitle(_translate("Dialog_showfitting", "拟合直线", None))

from pyqtgraph import PlotWidget
