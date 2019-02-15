# -*- coding=utf-8 -*-

from PyQt4 import QtGui, QtCore
from UiPy_MainWindow import Ui_MainWindow
from UiPy_Dialog_paramconfig import Ui_Dialog_paramconfig
import numpy as np
import struct
import os
from scipy import signal
import pyqtgraph as pg
import time
import sys
import posix_ipc as posix

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class Code_Dialog_paramconfig(Ui_Dialog_paramconfig):
    signal_getparamconfig = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        super(Code_Dialog_paramconfig, self).__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.signal_emitter)

    def signal_emitter(self):
        dict_paramconfig = {}
        dict_paramconfig['cable_length'] = float(self.lineEdit_cablelength.text())
        dict_paramconfig['sensor1_loc'] = float(self.lineEdit_sensor1loc.text())
        dict_paramconfig['sensor2_loc'] = float(self.lineEdit_sensor2loc.text())
        dict_paramconfig['speed_compensate'] = float(self.lineEdit_speedcompensate.text())
        self.signal_getparamconfig.emit(dict_paramconfig)

class Code_MainWindow(Ui_MainWindow):

    def __init__(self, parent=None):
        self.cable_length = 200
        self.sensor1_loc = 0
        self.sensor2_loc = 200
        self.speed_compensate = 1

        super(Code_MainWindow, self).__init__()
        self.setupUi(self)
        self.showMaximized();
        self.centralwidget.setLayout(self.gridLayout_figure)

        self.GLW_waveform.addLegend(offset=(-10,-70))
        self.GLW_waveform.setLabel('left', "voltage/V")
        self.GLW_waveform.setLabel('bottom', "time/t")
        self.GLW_waveform.setTitle('waveform')
        self.GLW_waveform.setDownsampling(ds=256,auto=False, mode='subsample')
        self.curve_waveform1=pg.PlotDataItem(pen='g',name = 'ch1')
        self.curve_waveform2=pg.PlotDataItem(pen='b',name = 'ch2')
        self.GLW_waveform.addItem(self.curve_waveform1)
        self.GLW_waveform.addItem(self.curve_waveform2)

        self.GLW_spectrum.addLegend(offset=(-10,-70))
        self.GLW_spectrum.setLabel('left', "amplitude/V")
        self.GLW_spectrum.setLabel('bottom', "frequency/khz")
        self.GLW_spectrum.setTitle('spectrum')
        self.curve_spectrum1=pg.PlotDataItem(pen='g',name = 'ch1')
        self.curve_spectrum2=pg.PlotDataItem(pen='b',name = 'ch2')
        self.GLW_spectrum.addItem(self.curve_spectrum1)
        self.GLW_spectrum.addItem(self.curve_spectrum2)

        self.GLW_localization.hideAxis('left')
        self.GLW_localization.hideAxis('bottom')
        self.marker_source=pg.PlotDataItem([self.sensor1_loc],[0],symbolBrush='r')
        self.marker_sensor1=pg.PlotDataItem([self.sensor1_loc],[0],symbolBrush='g')
        self.marker_sensor2=pg.PlotDataItem([self.sensor2_loc],[0],symbolBrush='g')
        self.line_cable=pg.PlotDataItem([0,self.cable_length],[0,0],pen='b')
        self.GLW_localization.setRange(QtCore.QRectF(0,0,self.cable_length,0))
        self.GLW_localization.addItem(self.line_cable)
        self.GLW_localization.addItem(self.marker_source)
        self.GLW_localization.addItem(self.marker_sensor1)
        self.GLW_localization.addItem(self.marker_sensor2)
        self.text_source = pg.TextItem(anchor=(0.5,0))
        self.text_sensor1 = pg.TextItem(text="sensor1",anchor=(0.5,0))
        self.text_sensor2 = pg.TextItem(text="sensor2",anchor=(0.5,0))
        self.text_sensor1.setPos(self.sensor1_loc,0)
        self.text_sensor2.setPos(self.sensor2_loc,0)
        self.GLW_localization.addItem(self.text_source)
        self.GLW_localization.addItem(self.text_sensor1)
        self.GLW_localization.addItem(self.text_sensor2)
        self.GLW_localization.setMouseEnabled(x=False, y=False)

        self.action_paramconfig.triggered.connect(self.open_paramconfig_dlg)

        path = os.getcwd() + "//" + "input_data" +"//" + "6" + "//" + "100" + "//" + '0'
        self.draw_waveform_spectrum(path)

    def open_paramconfig_dlg(self):
        self.ui_paramconfig = Code_Dialog_paramconfig()
        self.ui_paramconfig.lineEdit_cablelength.setText(str(self.cable_length))
        self.ui_paramconfig.lineEdit_sensor1loc.setText(str(self.sensor1_loc))
        self.ui_paramconfig.lineEdit_sensor2loc.setText(str(self.sensor2_loc))
        self.ui_paramconfig.lineEdit_sensor3loc.setText("0")
        self.ui_paramconfig.lineEdit_sensor4loc.setText("0")
        self.ui_paramconfig.lineEdit_speedcompensate.setText(str(self.speed_compensate))
        self.ui_paramconfig.show()
        self.ui_paramconfig.signal_getparamconfig.connect(self.get_paramconfig_dict)

    @QtCore.pyqtSlot(dict)
    def get_paramconfig_dict(self,dict_paramconfig):
        self.cable_length = dict_paramconfig['cable_length']
        self.sensor1_loc = dict_paramconfig['sensor1_loc']
        self.sensor2_loc = dict_paramconfig['sensor2_loc']
        self.text_sensor1.setPos(self.sensor1_loc,0)
        self.text_sensor2.setPos(self.sensor2_loc,0)
        self.line_cable.setData([0,self.cable_length],[0,0])
        self.marker_source.setData([self.sensor1_loc],[0])
        self.marker_sensor1.setData([self.sensor1_loc],[0])
        self.marker_sensor2.setData([self.sensor2_loc],[0])
        self.GLW_localization.setRange(QtCore.QRectF(0,0,self.cable_length,0))
    
    def draw_waveform_spectrum(self,path):
        pwd = os.getcwd()
        fb = open(path, "rb")
        count = 0
        datax = []
        datay1 = []
        datay2 = []
        while True:
            data = fb.read(4)
            if not data:
                break
            ch1, ch2 = struct.unpack('<HH', data)
            ch1 = (float(ch1) - 8192) / 8192 * 2.5
            ch2 = (float(ch2) - 8192) / 8192 * 2.5
            datax.append(count * 0.0000001)
            datay1.append(ch1)
            datay2.append(ch2)
            count = count + 1

        fb.close()

        self.curve_waveform1.setData(datax,datay1)
        self.curve_waveform2.setData(datax,datay2)

        datay1 = datay1[200000:700000]
        datay1 = datay2[200000:700000]

        fftnum = 8192
        std = 1500
        fftrepeat = 0

        axis_xf = range(int(fftnum/2))
        freq = [i * 10000000.0 / fftnum for i in axis_xf]

        index = 0
        magnitude1 = np.zeros(fftnum)
        magnitude2 = np.zeros(fftnum)
        while True:
            data1 = np.array(datay1[index:index + fftnum])
            data2 = np.array(datay2[index:index + fftnum])
            win = signal.gaussian(fftnum, std)
            data1 = np.multiply(data1,win)
            data2 = np.multiply(data2,win)
            data1 = np.abs(np.fft.fft(data1, fftnum))
            data2 = np.abs(np.fft.fft(data2, fftnum))
            magnitude1 += data1
            magnitude2 += data2
            index += int(fftnum * (1 - fftrepeat))
            if index + fftnum > len(datay1):
                break

        start = int(fftnum / 500)
        end = int(fftnum / 25)

        magnitude1 = magnitude1[start:end]
        maxmag1 = max(magnitude1)
        magnitude1 = magnitude1 / maxmag1

        magnitude2 = magnitude2[start:end]
        maxmag2 = max(magnitude2)
        magnitude2 = magnitude2 / maxmag2

        freq = np.array(freq[start:end])
        freq = freq/1000

        self.curve_spectrum1.setData(freq,magnitude1)
        self.curve_spectrum2.setData(freq,magnitude2)

        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s.%03d" % (data_head, data_secs) + "  位置90cm处  " + "断丝概率60%"
        self.textEdit_record.setText(time_stamp)

        self.marker_source.setData([40],[0])
        self.text_source.setPos(40,0)
        self.text_source.setText(str(40)+"cm")

def main():
    os.system("./out1 &")
    app = QtGui.QApplication(sys.argv)
    ui_main = Code_MainWindow()
    ui_main.show()
    ret=app.exec_()
    mq=posix.MessageQueue("/mq1")
    mesg,_=mq.receive()
    print(mesg.decode())
    os.system("pkill out1")
    mq.close()
    posix.unlink_message_queue("/mq1")
    sys.exit(ret)

if __name__ == "__main__":
    main()
