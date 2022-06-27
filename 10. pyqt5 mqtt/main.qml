import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import QtQuick.Extras.Private 1.0
//import "E:\python\pyqt\benchmark\qml\controls"

Item {
    width: 640
    height: 480
    visible: true
    //title: qsTr("Hello World")

    function updateValue(){
        text2.text = mqttvalue.speedinput1()
        text4.text = mqttvalue.speedinput2()
    }

	



    Rectangle {
        id: rectangle
        x: 0
        y: 0
        width: 640
        height: 480
        color: "#ffff00"
    }

    Text {
        id: text1
        x: 71
        y: 78
        text: qsTr("data 1:")
        font.pixelSize: 12
    }


    Text {
        id: text2
        x: 119
        y: 77
        width: 21
        height: 15
        //text: qsTr("000")
        font.pixelSize: 12
    }



    Text {
        id: text3
        x: 71
        y: 97
        text: qsTr("data 2 :")
        font.pixelSize: 12
    }

    Text {
        id: text4
        x: 119
        y: 97
        text: qsTr("000")
        font.pixelSize: 12
    }

/*

	CustomSwitch{
		id: ledSwitch3
		anchors.left: parent.left
		anchors.leftMargin: 120
		anchors.top: parent.top
        anchors.topMargin: 200
		backgroundHeight: 30
		backgroundWidth: 100
		colorbg: "#f73924" 
		}
*/
}
