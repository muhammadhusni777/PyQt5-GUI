from PyQt5.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot, QTimer, pyqtProperty
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QQmlApplicationEngine

import sys
import time
import paho.mqtt.client as paho
#broker="123.45.0.10"


broker="broker.emqx.io"#"127.0.0.1"
port = 1883

S1 = 0
S2 = 0


class MQTTValue(QObject):  
    def __init__(self):
        super(MQTTValue,self).__init__()
    
    @pyqtSlot(result=float)
    def speedinput1(self):  return S1
    
    @pyqtSlot(result=float)
    def speedinput2(self):  return S2




def on_message(client, userdata, message):
        msg = str(message.payload.decode("utf-8"))
        t = str(message.topic)

        if(msg[0] == 'c'):
            val =  1
        else:
            val = int(msg)

        if (t == "speedinput1"):
            global S1
            S1 = float(msg)
            print(S1)
        
        if (t == "speedinput2"):
            global S2
            S2 = float(msg)
        


if __name__ == "__main__":
    
    client= paho.Client("GUI")
    client.on_message=on_message

    print("connecting to broker ",broker)
    client.connect(broker,port)#connect
    print(broker," connected")


    client.loop_start()
    print("Subscribing")
    
    client.subscribe("speedinput1")
    client.subscribe("speedinput2")
    
    
    

    ## QT5 GUI
    print("Graphical User Interface ")
    app = QGuiApplication(sys.argv)

    view = QQuickView()
    view.setSource(QUrl('main.qml'))

    mqttvalue = MQTTValue()


    timer = QTimer()
    timer.start(10) ##Update screen every 10 miliseconds

    context = view.rootContext()
    context.setContextProperty("mqttvalue", mqttvalue)

    root = view.rootObject()
    timer.timeout.connect(root.updateValue) ##Call function update in GUI QML

    engine = QQmlApplicationEngine(app) 
    engine.quit.connect(app.quit) ## Quit Button Respon
        
    view.show()

    sys.exit(app.exec_())
