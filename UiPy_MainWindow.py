# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
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

class Ui_MainWindow(QtGui.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(752, 547)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 731, 481))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout_figure = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_figure.setObjectName(_fromUtf8("gridLayout_figure"))
        self.GLW_waveform = PlotWidget(self.gridLayoutWidget)
        self.GLW_waveform.setObjectName(_fromUtf8("GLW_waveform"))
        self.gridLayout_figure.addWidget(self.GLW_waveform, 0, 0, 1, 3)
        self.btn_showhis = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_showhis.sizePolicy().hasHeightForWidth())
        self.btn_showhis.setSizePolicy(sizePolicy)
        self.btn_showhis.setObjectName(_fromUtf8("btn_showhis"))
        self.gridLayout_figure.addWidget(self.btn_showhis, 2, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_figure.addItem(spacerItem, 2, 1, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_figure.addWidget(self.label, 2, 0, 1, 1)
        self.GLW_spectrum = PlotWidget(self.gridLayoutWidget)
        self.GLW_spectrum.setObjectName(_fromUtf8("GLW_spectrum"))
        self.gridLayout_figure.addWidget(self.GLW_spectrum, 1, 0, 1, 1)
        self.GLW_localization = PlotWidget(self.gridLayoutWidget)
        self.GLW_localization.setObjectName(_fromUtf8("GLW_localization"))
        self.gridLayout_figure.addWidget(self.GLW_localization, 1, 1, 1, 2)
        self.textEdit_record = QtGui.QTextEdit(self.gridLayoutWidget)
        self.textEdit_record.setObjectName(_fromUtf8("textEdit_record"))
        self.gridLayout_figure.addWidget(self.textEdit_record, 3, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 752, 31))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_capture = QtGui.QMenu(self.menubar)
        self.menu_capture.setObjectName(_fromUtf8("menu_capture"))
        self.menu_analysis = QtGui.QMenu(self.menubar)
        self.menu_analysis.setObjectName(_fromUtf8("menu_analysis"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_startcapture = QtGui.QAction(MainWindow)
        self.action_startcapture.setObjectName(_fromUtf8("action_startcapture"))
        self.action_channelconfig = QtGui.QAction(MainWindow)
        self.action_channelconfig.setObjectName(_fromUtf8("action_channelconfig"))
        self.action_showhis = QtGui.QAction(MainWindow)
        self.action_showhis.setObjectName(_fromUtf8("action_showhis"))
        self.action_5 = QtGui.QAction(MainWindow)
        self.action_5.setObjectName(_fromUtf8("action_5"))
        self.action_cableparam = QtGui.QAction(MainWindow)
        self.action_cableparam.setObjectName(_fromUtf8("action_cableparam"))
        self.menu_capture.addSeparator()
        self.menu_capture.addAction(self.action_startcapture)
        self.menu_capture.addAction(self.action_channelconfig)
        self.menu_analysis.addAction(self.action_showhis)
        self.menu_analysis.addAction(self.action_cableparam)
        self.menubar.addAction(self.menu_capture.menuAction())
        self.menubar.addAction(self.menu_analysis.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btn_showhis.setText(_translate("MainWindow", "查看历史", None))
        self.label.setText(_translate("MainWindow", "记录", None))
        self.menu_capture.setTitle(_translate("MainWindow", "采集设置", None))
        self.menu_analysis.setTitle(_translate("MainWindow", "分析设置", None))
        self.action_startcapture.setText(_translate("MainWindow", "开始采集", None))
        self.action_channelconfig.setText(_translate("MainWindow", "通道配置", None))
        self.action_showhis.setText(_translate("MainWindow", "查看历史", None))
        self.action_5.setText(_translate("MainWindow", "参数配置", None))
        self.action_cableparam.setText(_translate("MainWindow", "缆索参数", None))

from pyqtgraph import PlotWidget
