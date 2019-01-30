# -*- coding=utf-8 -*-

from PyQt4 import QtGui, QtCore
from UiPy_MainWindow import Ui_MainWindow
import numpy as np
import struct
import os
from scipy import signal
import pyqtgraph as pg
import time


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class Code_MainWindow(Ui_MainWindow):

    def __init__(self, parent=None):
        super(Code_MainWindow, self).__init__()
        self.setupUi(self)
        self.showMaximized();
        self.centralwidget.setLayout(self.gridLayout_figure)
       
        path = os.getcwd() + "//" + "input_data" +"//" + "6" + "//" + "100" + "//" + '0'

        self.draw_waveform_spectrum(path)

    
    def draw_waveform_spectrum(self,path):
        pwd = os.getcwd()
        fb = open(path, "rb")
        count = 0
        datax = []
        datay1 = []
        datay2 = []
        interval = 500
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

        self.GLW_localization.hideAxis('left')
        self.GLW_localization.hideAxis('bottom')
        cable=pg.PlotDataItem([0,100],[0,0],pen='b')
        source=pg.PlotDataItem([40],[0],pen='r',symbolBrush=(255,0,0), symbolPen='w')
        sensor1=pg.PlotDataItem([0],[0],pen='r',symbolBrush=(0,255,0), symbolPen='w')
        sensor2=pg.PlotDataItem([100],[0],pen='r',symbolBrush=(0,255,0), symbolPen='w')
        self.GLW_localization.setRange(QtCore.QRectF(0,0,100,0))

        self.GLW_localization.addItem(cable)
        self.GLW_localization.addItem(source)
        self.GLW_localization.addItem(sensor1)
        self.GLW_localization.addItem(sensor2)

        self.GLW_waveform.addLegend(offset=(-10,-70))
        #datax = datax[1:count:interval]
        #self.GLW_waveform.plot(datax,datay1[1:count:interval],pen='g',name = 'ch1')
        #self.GLW_waveform.plot(datax,datay2[1:count:interval],pen='b',name = 'ch2')
        self.GLW_waveform.plot(datax,datay1,pen='g',name = 'ch1')
        self.GLW_waveform.plot(datax,datay2,pen='b',name = 'ch2')
        self.GLW_waveform.setDownsampling(ds=512,auto=False, mode='subsample')

        self.GLW_waveform.setLabel('left', "voltage/V")
        self.GLW_waveform.setLabel('bottom', "time/t")
        self.GLW_waveform.setTitle('waveform')

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

        self.GLW_spectrum.addLegend(offset=(-10,-70))
        self.GLW_spectrum.plot(freq,magnitude1,pen='g',name = 'ch1')
        self.GLW_spectrum.plot(freq,magnitude2,pen='b',name = 'ch2')

        self.GLW_spectrum.setLabel('left', "amplitude/V")
        self.GLW_spectrum.setLabel('bottom', "frequency/khz")
        self.GLW_spectrum.setTitle('spectrum')

        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s.%03d" % (data_head, data_secs) + "  位置90cm处  " + "断丝概率60%"
        self.textEdit_record.setText(time_stamp)

        text_source = pg.TextItem(text="(40,0)",anchor=(0.5,1))
        self.GLW_localization.addItem(text_source)
        text_source.setPos(40,0)



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui_main = Code_MainWindow()
    ui_main.show()
sys.exit(app.exec_())
