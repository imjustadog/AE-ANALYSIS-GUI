# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from UiPy_Dialog_calibration import Ui_Dialog_calibration
from UiPy_Dialog_showfitting import Ui_Dialog_showfitting
import numpy as np
import struct
import os
from scipy import signal
import time
import sys
import posix_ipc as posix
import threading
import pywt
from math import pi,sqrt
import pyqtgraph as pg


class Code_Dialog_showfitting(Ui_Dialog_showfitting):
    signal_showfitting = QtCore.pyqtSignal(list)

    def __init__(self,parent=None):
        super(Code_Dialog_showfitting, self).__init__()
        self.setupUi(self)
        self.widget.setLabel('left', "time difference/ms")
        self.widget.setLabel('bottom', "location/cm")
        self.widget.setTitle("linear fitting")
        self.fitting_line=pg.PlotDataItem(pen='b')
        self.data_points=pg.ScatterPlotItem(brush='r')
        self.widget.addItem(self.fitting_line)
        self.widget.addItem(self.data_points)
        self.signal_showfitting.connect(self.showfitting)
    
    @QtCore.pyqtSlot(list)
    def showfitting(self,data):
        x = np.array(data[0])
        y = np.array(data[1])
        self.data_points.setData(x,y)
        func = np.polyfit(x,y,1)
        yf = func[0] * x + func[1]
        self.fitting_line.setData(x,yf)

class Code_Dialog_calibration(Ui_Dialog_calibration):
    signal_calculatecorr = QtCore.pyqtSignal(str)
    signal_calibrate = QtCore.pyqtSignal(str)
    signal_getcalibration = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(Code_Dialog_calibration, self).__init__()
        self.setupUi(self)
        self.mqd = ""
        self.mqf = ""
        self.dict_fitting = {}
        self.pushButton_start_to_capture.clicked.connect(self.start_to_capture)
        self.pushButton_stop_to_capture.clicked.connect(self.stop_capture)
        self.pushButton_change_location.clicked.connect(self.change_location)
        self.pushButton_calculate.clicked.connect(self.calculate)
        self.checkBox_choose_path.stateChanged.connect(self.set_path_choose)
        self.signal_calibrate.connect(self.calibrate)
        self.signal_calculatecorr.connect(self.calculatecorr)
        self.pushButton_start_to_capture.setEnabled(True)
        self.pushButton_stop_to_capture.setEnabled(False)

    def start_to_capture(self):
        if self.lineEdit_sensor1_location.text() == "":
            result = QtGui.QMessageBox.warning(self, "warning", "please input sensor1's location first")
            return
        if self.lineEdit_sensor2_location.text() == "":
            result = QtGui.QMessageBox.warning(self, "warning", "please input sensor2's location first")
            return
        if self.lineEdit_source_location.text() == "":
            result = QtGui.QMessageBox.warning(self, "warning", "please input source's location first")
            return
        self.sensor1_loc = float(self.lineEdit_sensor1_location.text())
        self.sensor2_loc = float(self.lineEdit_sensor2_location.text())
        self.source_loc = float(self.lineEdit_source_location.text())
        self.lineEdit_sensor1_location.setEnabled(False)
        self.lineEdit_sensor2_location.setEnabled(False)
        self.lineEdit_source_location.setEnabled(False)
        
        self.running = threading.Event()
        self.flag = threading.Event()
        self.running.set()
        self.flag.clear()
        self.receive_thread = threading.Thread(name = "datareceiver", target = self.receive_message_queue)
        self.receive_thread.start()

        self.pushButton_start_to_capture.setEnabled(False)
        self.pushButton_stop_to_capture.setEnabled(True)
        
        self.mqd=posix.MessageQueue("/mqcd", flags=posix.O_CREAT, mode=0o644)
        self.mqf=posix.MessageQueue("/mqcf", flags=posix.O_CREAT, mode=0o644)
        self.start_capture()
    
    def change_location(self):
        self.lineEdit_sensor1_location.setEnabled(True)
        self.lineEdit_sensor2_location.setEnabled(True)
        self.lineEdit_source_location.setEnabled(True)
        self.stop_capture()

    def start_capture(self):
        self.dict_fitting[self.source_loc] = []
        os.system("./caliread xillybus_read1_32 card1_cali/%d &"%(self.source_loc * 100))
        #os.system("./out1 card1_cali %d &"%(self.source_loc * 100))
        mesg,_=self.mqd.receive()
        mesg_receive = mesg.decode()
        if mesg_receive[0] == 'x' :
            result = QtGui.QMessageBox.warning(self,
                      "warning",
                      "please insert PCIe device")
        else:
            self.label_capture_count.setText("第0次采集完成")
            self.flag.set()

    def stop_capture(self):
        self.pushButton_start_to_capture.setEnabled(True)
        self.pushButton_stop_to_capture.setEnabled(False)
        self.flag.clear()
        os.system("pkill caliread")
        #os.system("pkill out1")

    def receive_message_queue(self):
        while self.running.isSet():
            self.flag.wait()
            mesg,_=self.mqf.receive()
            filepath = mesg.decode()
            if os.path.exists(filepath):
                count_now = int(filepath.split("/")[2])
                self.label_capture_count.setText("第%d次采集完成"%(count_now))
                self.signal_calculatecorr.emit(filepath)

    @QtCore.pyqtSlot(int)
    def set_path_choose(self,state):
        if state != 0:
            self.lineEdit_path.setEnabled(True)
            self.pushButton_choose_path.setEnabled(True)
            self.lineEdit_sensor1_location.setEnabled(False)
            self.lineEdit_sensor2_location.setEnabled(False)
            self.lineEdit_source_location.setEnabled(False)  
            self.pushButton_start_to_capture.setEnabled(False)  
            self.pushButton_change_location.setEnabled(False)
            self.textEdit_time_difference.setEnabled(False) 
            self.comboBox_choose_card.setEnabled(False)     
        else:
            self.lineEdit_path.setEnabled(False)
            self.pushButton_choose_path.setEnabled(False)
            self.lineEdit_sensor1_location.setEnabled(True)
            self.lineEdit_sensor2_location.setEnabled(True)
            self.lineEdit_source_location.setEnabled(True)  
            self.pushButton_start_to_capture.setEnabled(True)  
            self.pushButton_change_location.setEnabled(True)
            self.textEdit_time_difference.setEnabled(True) 
            self.comboBox_choose_card.setEnabled(True)

    def calculate(self):
        if self.lineEdit_path.isEnabled():
            self.signal_calibrate.emit(self.lineEdit_path.text())
        else:
            self.signal_calibrate.emit("card1_cali")

    @QtCore.pyqtSlot(str)
    def calculatecorr(self,filepath):
        
        interval = 5
        dt = 0.0000001 * interval
        fs = 10000000 / interval
        start = 250000
        end = 350000
        
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
        fa = np.arange(20000, 400000 + 1, 10000)
        scales = np.array(float(c)) * fs / np.array(fa)

        [cfs1,frequencies1] = pywt.cwt(data1,scales,wavelet,dt)
        [cfs2,frequencies2] = pywt.cwt(data2,scales,wavelet,dt)
        power1 = (abs(cfs1)) ** 2
        power2 = (abs(cfs2)) ** 2

        for i,f in enumerate(fa):
            mean1 = power1[i].mean()
            power1[i] = power1[i] / mean1
            mean2 =  power2[i].mean()
            power2[i] = power2[i] / mean2
            temp = signal.correlate(power1[i],power2[i], mode='same',method='fft')
            corr = (np.where(temp == max(temp))[0][0]-len(temp) / 2 ) * dt * 1000
            self.dict_fitting[self.source_loc].append([f, corr])
        
        showdict = ""
        for item in sorted(self.dict_fitting[self.source_loc]):
            showdict += "freq:%dHz corr:%.4fms\r\n"%(item[0],item[1])
        self.textEdit_time_difference.setText(showdict)

    @QtCore.pyqtSlot(str)
    def calibrate(self,filepath):

        interval = 5
        dt = 0.0000001 * interval
        fs = 10000000 / interval
        start = 250000
        end = 350000
        fa = np.arange(20000, 400000 + 1, 10000)

        dict_fitting = {}
        for f in fa:
            dict_fitting[f] = []
            dict_fitting[f].append([])
            dict_fitting[f].append([])
            dict_fitting[f].append([0])

        filelisttemp = os.listdir(filepath)
        for filename in filelisttemp:
            if os.path.isdir(filepath + "/" + filename):
                dd = int(filename)
                countlisttemp = os.listdir(filepath + "/" + filename)
                for count in countlisttemp:
                    if int(count) > 10:
                        continue
                    path = filepath + "/" + filename + "/" + count
                    with open(path, "rb") as fb:
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
                    scales = np.array(float(c)) * fs / np.array(fa)

                    [cfs1,frequencies1] = pywt.cwt(data1,scales,wavelet,dt)
                    [cfs2,frequencies2] = pywt.cwt(data2,scales,wavelet,dt)
                    power1 = (abs(cfs1)) ** 2
                    power2 = (abs(cfs2)) ** 2
        
                    flag = 0
                    for i,f in enumerate(fa):
                        mean1 = power1[i].mean()
                        power1[i] = power1[i] / mean1
                        mean2 =  power2[i].mean()
                        power2[i] = power2[i] / mean2
                        temp = signal.correlate(power1[i],power2[i], mode='same',method='fft')
                        corr = (np.where(temp == max(temp))[0][0]-len(temp) / 2 ) * dt * 1000
                        if dd != 100 and corr == 0:
                            dict_fitting[f][2] = 1
                        dict_fitting[f][0].append(dd)
                        dict_fitting[f][1].append(corr)

                    print(path)

        result = {}
        for f in dict_fitting.keys():
            x = np.array(dict_fitting[f][0])
            y = np.array(dict_fitting[f][1])
            func = np.polyfit(x,y,1)
            yf = x * func[0] + func[1]
            error = np.mean((yf - y) ** 2)
            #if error > 0 and dict_fitting[f][2] != 1:
            result[f] = error
        
        freq,error = min(result.items(), key=lambda x: x[1])
        self.lineEdit_best_frequency.setText(str(freq))

        x = np.array(dict_fitting[freq][0])
        y = np.array(dict_fitting[freq][1])
        func = np.polyfit(x,y,1)
        self.freq = freq
        self.speed = 20.0 / func[0]
        self.lineEdit_acoustic_speed.setText("%.1f"%(self.speed))

        self.ui_fitting = Code_Dialog_showfitting()
        self.ui_fitting.show()
        self.ui_fitting.signal_showfitting.emit(dict_fitting[freq])

    def closeEvent(self,event):
        self.signal_getcalibration.emit([self.lineEdit_acoustic_speed.text(),self.lineEdit_best_frequency.text()])
        event.accept()
        #os.system("pkill out1")
        os.system("pkill caliread")
        if self.mqd != "":
            self.mqd.close()
            posix.unlink_message_queue("/mqcd")
            self.mqd = ""
        if self.mqf != "":
            self.mqf.close()
            posix.unlink_message_queue("/mqcf")
            self.mqf = ""

def main():
    app = QtGui.QApplication(sys.argv)
    ui_calibration = Code_Dialog_calibration()
    ui_calibration.show()
    ret=app.exec_()
    ui_calibration.flag.set()
    ui_calibration.running.clear()
    #os.system("pkill out1")
    os.system("pkill caliread")
    if ui_calibration.mqd != "":
        ui_calibration.mqd.close()
        posix.unlink_message_queue("/mqcd")
    if ui_calibration.mqf != "":
        ui_calibration.mqf.close()
        posix.unlink_message_queue("/mqcf")
    sys.exit(ret)
    os._exit(0)

if __name__ == "__main__":
    main()
