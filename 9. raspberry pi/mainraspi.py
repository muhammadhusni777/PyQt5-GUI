import sys

from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot, QTimer, pyqtProperty
from PyQt5.QtCore    import pyqtSlot, pyqtSignal, QUrl, QObject,QStringListModel, Qt
from PyQt5.QtQuick   import QQuickView
from PyQt5.QtWidgets import QApplication, QCheckBox, QGridLayout, QGroupBox
from PyQt5.QtWidgets import QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QSlider
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QGuiApplication, QIcon

import time

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(20,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(16,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)



adc = 0
data1 = 0
data2 = 0
esp32_status = "inactive"

time_esp = 0
time_esp_prev = time.time()

sensor1_color = "#04f8fa" #"#df1c39"
sensor2_color = "#04f8fa" #"#df1c39"


datapinpwm = 0
formchar = "0"

led_status1 = "off"
led_status2 = "off"
led_status3 = "off"


message_time = 0
message_time_prev = time.time()


@pyqtSlot(result=int)
def get_tempo(self):
    date_time = QDateTime.currentDateTime()
    unixTIME = date_time.toSecsSinceEpoch()
    print("yes")
    #unixTIMEx = date_time.currentMSecsSinceEpoch()
    return unixTIME



class table(QQuickView):
    adc_val = pyqtSignal(str)
    sensor1_color_val = pyqtSignal(str)
    sensor2_color_val = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setSource(QUrl('mainraspi.qml'))
        self.setTitle("")
        
        self.rootContext().setContextProperty("table", self)
        self.setGeometry(100, 100, 1000, 600)
        self.show()
        
        windows = self.rootObject()
        
        self.init_tempo()
        
        self.adc_val.connect(windows.adc_read)
        self.sensor1_color_val.connect(windows.sensor1_color_read)
        self.sensor2_color_val.connect(windows.sensor2_color_read)


    def init_tempo(self):
        self.tempo = QtCore.QTimer()
        self.tempo.timeout.connect(self.variable_transfer)
        self.tempo.start(500)
        
        
    def variable_transfer(self):
        global time_esp
        global espledcolor
        global message_time
        global message_time_prev
        global sensor1_color
        global sensor2_color
        
        time_esp = time.time() - time_esp_prev
        
        
        self.adc_val.emit(str(adc))
        self.sensor1_color_val.emit(str(sensor1_color))
        self.sensor2_color_val.emit(str(sensor2_color))
        
        self.tempo.start(50)
        
        message_time = time.time() - message_time_prev

        if (message_time > 0.5):
            print(" | pwm : " + str(datapinpwm) +  " | led1 : " +
                  str(led_status1) +  " | led2 : " +
               str(led_status2)
                  +  " | led3 :" +
                  str(led_status3))
                
            message_time_prev = time.time()
        
        if(GPIO.input(20)==GPIO.HIGH):
            sensor1_color = "#04f8fa" #"#df1c39"
        else:
            sensor1_color = "#df1c39"
        
        if(GPIO.input(16)==GPIO.HIGH):
            sensor2_color = "#04f8fa" #"#df1c39"
        else:
            sensor2_color = "#df1c39"
        
        
        
        
        if(led_status1 =='on'):
            GPIO.output(21,GPIO.HIGH)
        #print(led_status)
        if(led_status1 == 'off'):
            GPIO.output(21,GPIO.LOW)   
    
    @pyqtSlot('QString')
    def setPwm(self, value):
        global datapinpwm
        datapinpwm = value
        #print(datapinpwm)
    
    @pyqtSlot('QString')
    def form_char(self, value):
        global formchar
        formchar = value
        #print(formchar)
    
    @pyqtSlot('QString')
    def led_status1(self, value):
        global led_status1
        led_status1 = value
    
    @pyqtSlot('QString')
    def led_status2(self, value):
        global led_status2
        led_status2 = value
        
    @pyqtSlot('QString')
    def led_status3(self, value):
        global led_status3
        led_status3 = value
            


if __name__ == '__main__':
    
    app = QApplication(sys.argv)    
    w = table()
    sys.exit(app.exec_())