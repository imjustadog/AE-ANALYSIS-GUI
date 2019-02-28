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
import threading
import pywt

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
    signal_drawwavespec = QtCore.pyqtSignal(str)

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
        self.GLW_waveform.setDownsampling(ds=512,auto=False, mode='subsample')
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
        self.action_startcapture.triggered.connect(self.start_capture)
        self.action_stopcapture.triggered.connect(self.stop_capture)
        self.signal_drawwavespec.connect(self.draw_wavespec_str)

        self.log_analysis = ""

        self.running = threading.Event()
        self.flag = threading.Event()
        self.running.set()
        self.flag.clear()
        self.receive_thread = threading.Thread(name = "datareceiver", target = self.receive_message_queue)
        self.receive_thread.start()
        
        self.mqd=posix.MessageQueue("/mqd", flags=posix.O_CREAT, mode=0o644)
        self.mqf=posix.MessageQueue("/mqf", flags=posix.O_CREAT, mode=0o644)

        #path = os.getcwd() + "//" + "input_data" +"//" + "6" + "//" + "100" + "//" + '0'
        #self.draw_waveform_spectrum(path)

    @QtCore.pyqtSlot(str)
    def draw_wavespec_str(self,filepath):
        self.draw_waveform_spectrum(filepath)

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

    def start_capture(self):
        os.system("./streamread &")
        #os.system("./out1 &")
        mesg,_=self.mqd.receive()
        self.dirpath = mesg.decode()
        print(self.dirpath)
        self.flag.set()

    def stop_capture(self):
        self.flag.clear()
        os.system("pkill streamread")
        #os.system("pkill out1")

    def receive_message_queue(self):
        while self.running.isSet():
            self.flag.wait()
            mesg,_=self.mqf.receive()
            filepath = self.dirpath + "/" + mesg.decode()
            #filepath = "Thu_Feb_21_18-42-59_2019/2019-2-20_9-19-42_641"
            print(filepath)
            if os.path.exists(filepath):
                self.signal_drawwavespec.emit(filepath)
    
    def draw_waveform_spectrum(self,path):
        #timestart = time.time()
        #print("func start")
        
        datax = []
        datay1 = []
        datay2 = []

        with open(path, "rb") as fb:
            data = fb.read()

        ch1ch2 = struct.unpack("<"+str(int(len(data)/2))+"H", data)
        ch1ch2 = np.array(ch1ch2)
        ch1ch2 = (ch1ch2-8192)*2.5/8192

        datay1 = ch1ch2[::2]
        datay2 = ch1ch2[1::2]
        datax = np.array(range(len(datay1)))* 0.0000001

        #dataxd = datax[200000:700000:512]
        #self.curve_waveform1.setData(dataxd,datay1[200000:700000:512])
        #self.curve_waveform2.setData(dataxd,datay2[200000:700000:512])
        
        #print("read ok:%.2f"%(time.time() - timestart))
        self.curve_waveform1.setData(datax,datay1)
        self.curve_waveform2.setData(datax,datay2)
        #print("draw wave:%.2f"%(time.time() - timestart))

        datay1 = datay1[200000:700000]
        datay2 = datay2[200000:700000]

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
        #magnitude1 = np.abs(np.fft.fft(datay1))
        #magnitude2 = np.abs(np.fft.fft(datay2))
        #fftnum = len(magnitude1)
        #axis_xf = range(int(fftnum/2))
        #freq = [i * 10000000.0 / fftnum for i in axis_xf]
        start = int(fftnum / 500)
        end = int(fftnum / 25)
        magnitude1 = magnitude1[start:end]
        magnitude1 = magnitude1 / (fftnum / 2)
        magnitude2 = magnitude2[start:end]
        magnitude2 = magnitude2 / (fftnum / 2)
        freq = np.array(freq[start:end])
        freq = freq/1000
        self.curve_spectrum1.setData(freq,magnitude1)
        self.curve_spectrum2.setData(freq,magnitude2)
        #print("draw spec:%.2f"%(time.time() - timestart))

        dt = 0.0000001
        fs = 10000000
        datay1 = datay1[int(50000):int(150000)]
        datay2 = datay2[int(50000):int(150000)]
        wavelet = 'morl'
        c = pywt.central_frequency(wavelet)
        fa = [320000]
        scales = np.array(float(c)) * fs / np.array(fa)
        [cfs1,frequencies1] = pywt.cwt(datay1,scales,wavelet,dt)
        [cfs2,frequencies2] = pywt.cwt(datay2,scales,wavelet,dt)
        power1 = abs(cfs1)
        power2 = abs(cfs2)
        mean1 = power1[0].mean()
        power1[0] = power1[0] / mean1
        mean2 =  power2[0].mean()
        power2[0] = power2[0] / mean2
        temp = signal.correlate(power1[0],power2[0], mode='same',method='fft')
        corr=(np.where(temp == max(temp))[0][0]-len(temp) / 2 ) * dt * 1000
        location = (self.sensor1_loc + self.sensor2_loc - corr / 0.057 * 20) / 2

        _,log_datetime = path.split('/')
        log_datetime = log_datetime.split("_")
        log_datetime = log_datetime[0] + " " + ":".join(log_datetime[1].split('-')) + "." + log_datetime[2]
        self.log_analysis += log_datetime + "  时间差%f"%(corr) + "  位置%.1fcm处  \r\n"%(location) #+ "断丝概率%d%%"%(60) + "\r\n"
        self.textEdit_record.setText(self.log_analysis)
        self.textEdit_record.moveCursor(QtGui.QTextCursor.End)

        self.marker_source.setData([location],[0])
        self.text_source.setPos(location,0)
        self.text_source.setText("%.1fcm"%(location))
        #print("calc location:%.2f"%(time.time() - timestart))

    def closeEvent(self,event):
        event.accept()
        self.mqd.close()
        self.mqf.close()
        posix.unlink_message_queue("/mqd")
        posix.unlink_message_queue("/mqf")
        os._exit(0)

def main():
    app = QtGui.QApplication(sys.argv)
    ui_main = Code_MainWindow()
    ui_main.show()
    ret=app.exec_()
    ui_main.flag.set()
    ui_main.running.clear()
    ui_main.mqd.close()
    ui_main.mqf.close()
    posix.unlink_message_queue("/mqd")
    posix.unlink_message_queue("/mqf")
    sys.exit(ret)

if __name__ == "__main__":
    main()
