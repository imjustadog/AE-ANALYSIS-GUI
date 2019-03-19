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
from math import pi,sqrt

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
        dict_paramconfig['card1_acoustic_speed'] = float(self.lineEdit_card1_acoustic_speed.text())
        dict_paramconfig['card2_acoustic_speed'] = float(self.lineEdit_card2_acoustic_speed.text())
        self.signal_getparamconfig.emit(dict_paramconfig)

class Code_MainWindow(Ui_MainWindow):
    signal_drawwavespec = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        self.cable_length = 2
        self.sensor1_loc = 2
        self.sensor2_loc = 0
        self.card1_acoustic_speed =  200 / 0.057
        self.k0 = []
        self.k0_norm = []

        super(Code_MainWindow, self).__init__()
        self.setupUi(self)
        self.showMaximized();
        #self.tab_card1.setLayout(self.gridLayout_figure)

        self.lineEdit_card1_sensor1_location.setText(str(self.sensor1_loc))
        self.lineEdit_card1_sensor2_location.setText(str(self.sensor2_loc))
        self.lineEdit_card1_cable_length.setText(str(self.cable_length))
        self.lineEdit_card1_acoustic_speed.setText("%.3f"%(self.card1_acoustic_speed))

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
        self.text_sensor1.setText("sensor1\r\n%.1fm"%(self.sensor1_loc))
        self.text_sensor2.setText("sensor2\r\n%.1fm"%(self.sensor2_loc))
        self.GLW_localization.addItem(self.text_source)
        self.GLW_localization.addItem(self.text_sensor1)
        self.GLW_localization.addItem(self.text_sensor2)
        self.GLW_localization.setMouseEnabled(x=False, y=False)

        self.action_startcapture.setEnabled(True)
        self.action_stopcapture.setEnabled(False)

        self.pushButton_card1_config_ok.clicked.connect(self.change_card1_config)
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
        self.calc_k0()

        self.start_capture()

    def change_card1_config(self):
        self.cable_length = float(self.lineEdit_card1_cable_length.text())
        self.card1_acoustic_speed = float(self.lineEdit_card1_acoustic_speed.text())
        self.sensor1_loc = float(self.lineEdit_card1_sensor1_location.text())
        self.sensor2_loc = float(self.lineEdit_card1_sensor2_location.text())
        self.text_sensor1.setPos(self.sensor1_loc,0)
        self.text_sensor2.setPos(self.sensor2_loc,0)
        self.text_sensor1.setText("sensor1\r\n%.1fm"%(self.sensor1_loc))
        self.text_sensor2.setText("sensor2\r\n%.1fm"%(self.sensor2_loc))
        self.line_cable.setData([0,self.cable_length],[0,0])
        self.marker_source.setData([self.sensor1_loc],[0])
        self.marker_sensor1.setData([self.sensor1_loc],[0])
        self.marker_sensor2.setData([self.sensor2_loc],[0])
        self.GLW_localization.setRange(QtCore.QRectF(0,0,self.cable_length,0))
            

    @QtCore.pyqtSlot(str)
    def draw_wavespec_str(self,filepath):
        self.draw_waveform_spectrum(filepath)

    def open_paramconfig_dlg(self):
        self.ui_paramconfig = Code_Dialog_paramconfig()
        self.ui_paramconfig.lineEdit_card1_acoustic_speed.setText("%.1f"%(self.card1_acoustic_speed))
        self.ui_paramconfig.lineEdit_card2_acoustic_speed.setText("%.1f"%(self.card2_acoustic_speed))
        self.ui_paramconfig.show()
        self.ui_paramconfig.signal_getparamconfig.connect(self.get_paramconfig_dict)

    @QtCore.pyqtSlot(dict)
    def get_paramconfig_dict(self,dict_paramconfig):
        self.card1_acoustic_speed = dict_paramconfig['card1_acoustic_speed']
        self.card2_acoustic_speed = dict_paramconfig['card2_acoustic_speed']

    def start_capture(self):
        os.system("./streamread card1_data &")
        #os.system("./out1 &")
        mesg,_=self.mqd.receive()
        mesg_receive = mesg.decode()
        if mesg_receive[0] == 'x' :
            self.radioButton_card1_offline.setChecked(True)
        else:
            self.radioButton_card1_online.setChecked(True)
            self.action_startcapture.setEnabled(False)
            self.action_stopcapture.setEnabled(True)
            self.dirpath = mesg_receive
            print(self.dirpath)
            self.flag.set()

    def stop_capture(self):
        self.action_startcapture.setEnabled(True)
        self.action_stopcapture.setEnabled(False)
        self.flag.clear()
        os.system("pkill streamread")
        #os.system("pkill out1")

    def receive_message_queue(self):
        while self.running.isSet():
            self.flag.wait()
            mesg,_=self.mqf.receive()
            filepath = self.dirpath + "/" + mesg.decode()
            #filepath = "Thu_Feb_21_18-42-59_2019/2019-2-20_9-19-42_641"
            #print(filepath)
            if os.path.exists(filepath):
                self.signal_drawwavespec.emit(filepath)

    def calc_k0(self):
        fig_size = 20
        interval = 5
        dt = 0.0000001 * interval
        fs = 10000000 / interval
        start = 250000
        end = 350000
        path = "samples"
        filelisttemp = os.listdir(path)
        for filename in filelisttemp:
            filepath = path + "/" + filename
            with open(filepath, "rb") as fb:
                data = fb.read()
            ch1ch2 = struct.unpack("<"+str(int(len(data)/2))+"H", data)
            ch1ch2 = np.array(ch1ch2)
            ch1ch2 = (ch1ch2-8192)*2.5/8192
            datay1 = ch1ch2[::2]
            datay2 = ch1ch2[1::2]
            data1 = datay1[start:end:interval]
            data2 = datay2[start:end:interval]
            wavelet = 'morl'
            c = pywt.central_frequency(wavelet)
            fa = np.arange(400000, 20000 - 1, -20000)
            scales = np.array(float(c)) * fs / np.array(fa)
            [cfs1,frequencies1] = pywt.cwt(data1,scales,wavelet,dt)
            [cfs2,frequencies2] = pywt.cwt(data2,scales,wavelet,dt)
            power1 = (abs(cfs1)) ** 2
            power2 = (abs(cfs2)) ** 2
            length_now = len(power1[0])
            power1 = np.reshape(power1,(len(power1),fig_size,int(length_now/fig_size)))
            power2 = np.reshape(power2,(len(power2),fig_size,int(length_now/fig_size)))
            power1 = np.log10(np.mean(power1,axis=2))
            power2 = np.log10(np.mean(power2,axis=2))
            mx = power1.max()
            mn = power1.min()
            power1 = (power1-mn) / (mx-mn) * 255.0
            power1 = np.floor(power1)
            mx = power2.max()
            mn = power2.min()
            power2 = (power2-mn) / (mx-mn) * 255.0
            power2 = np.floor(power2)
            self.k0.append(power1)
            self.k0_norm.append(sqrt((power1 ** 2).sum()))
            self.k0.append(power2)
            self.k0_norm.append(sqrt((power2 ** 2).sum()))

    def calc_cos(self,k1,k2,k1_norm,k2_norm):
        max_cos = 0
        for index in range(len(self.k0_norm)):
            k0k1 = (self.k0[index] * k1).sum()
            cos1 = k0k1 / self.k0_norm[index] / k1_norm
            k0k2 = (self.k0[index] * k2).sum()
            cos2 = k0k2 / self.k0_norm[index] / k2_norm
            loss1 = 1 - cos1
            cos_dis1 = 1 - loss1 * 10
            loss2 = 1 - cos2
            cos_dis2 = 1 - loss2 * 10
            if cos_dis1 > max_cos:
                max_cos = cos_dis1
            if cos_dis2 > max_cos:
                max_cos = cos_dis2
        return max_cos
    
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
        corr=(np.where(temp == max(temp))[0][0]-len(temp) / 2 ) * dt
        location = (self.sensor1_loc + self.sensor2_loc - corr * self.card1_acoustic_speed) / 2

        datay1 = datay1[0:100000:5]
        datay2 = datay2[0:100000:5]
        dt = 0.0000001 * 5
        fs = 10000000 / 5
        fa = np.arange(400000, 20000 - 1, -20000)
        scales = np.array(float(c)) * fs / np.array(fa)
        [cfs1,frequencies1] = pywt.cwt(datay1,scales,wavelet,dt)
        [cfs2,frequencies2] = pywt.cwt(datay2,scales,wavelet,dt)
        power1 = (abs(cfs1)) ** 2
        power2 = (abs(cfs2)) ** 2
        length_now = len(power1[0])
        fig_size = 20
        power1 = np.reshape(power1,(len(power1),fig_size,int(length_now/fig_size)))
        power2 = np.reshape(power2,(len(power2),fig_size,int(length_now/fig_size)))
        power1 = np.log10(np.mean(power1,axis=2))
        power2 = np.log10(np.mean(power2,axis=2))
        mx = power1.max()
        mn = power1.min()
        power1 = (power1-mn) / (mx-mn) * 255.0
        power1 = np.floor(power1)
        mx = power2.max()
        mn = power2.min()
        power2 = (power2-mn) / (mx-mn) * 255.0
        power2 = np.floor(power2)
        power1_norm = sqrt((power1 ** 2).sum())
        power2_norm = sqrt((power2 ** 2).sum())
        cos_dis = self.calc_cos(power1,power2,power1_norm,power2_norm)

        _,_,log_datetime = path.split('/')
        log_datetime = log_datetime.split("_")
        log_datetime = log_datetime[0] + " " + ":".join(log_datetime[1].split('-')) + "." + log_datetime[2]
        self.log_analysis += log_datetime + "  时间差%fms"%(corr * 1000) + "  位置%.1fm处"%(location) + "  断丝概率%d%%"%(cos_dis * 100) + "\r\n"
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
