# Author: Mustafa Osman Dilmaç
# Simple PYQT6 GUI to read MPU6050 sensor data
# Update on 14/05/2024 -> Added simple ON/OFF buttons to control LED on ESP32

# -*- coding: utf-8 -*-

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QTimer)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLCDNumber, QLabel, QMainWindow,
    QMenuBar, QSizePolicy, QStatusBar, QWidget, QPushButton)
from PySide6 import QtWidgets
import time
import serial
from serial.tools import list_ports
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(690, 423)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.accelxLCD = QLCDNumber(self.centralwidget)
        self.accelxLCD.setObjectName(u"accelxLCD")
        self.accelxLCD.setGeometry(QRect(140, 30, 151, 41))
        self.accelyLCD = QLCDNumber(self.centralwidget)
        self.accelyLCD.setObjectName(u"accelyLCD")
        self.accelyLCD.setGeometry(QRect(140, 80, 151, 41))
        self.accelzLCD = QLCDNumber(self.centralwidget)
        self.accelzLCD.setObjectName(u"accelzLCD")
        self.accelzLCD.setGeometry(QRect(140, 130, 151, 41))
        self.gyrozLCD = QLCDNumber(self.centralwidget)
        self.gyrozLCD.setObjectName(u"gyrozLCD")
        self.gyrozLCD.setGeometry(QRect(460, 130, 151, 41))
        self.gyroxLCD = QLCDNumber(self.centralwidget)
        self.gyroxLCD.setObjectName(u"gyroxLCD")
        self.gyroxLCD.setGeometry(QRect(460, 30, 151, 41))
        self.gyroyLCD = QLCDNumber(self.centralwidget)
        self.gyroyLCD.setObjectName(u"gyroyLCD")
        self.gyroyLCD.setGeometry(QRect(460, 80, 151, 41))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(90, 40, 49, 16))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(90, 90, 49, 16))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(90, 140, 49, 16))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(410, 40, 49, 16))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(410, 90, 49, 16))
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(410, 140, 49, 16))
        
        # ON/OFF butonları
        self.ledOnButton = QPushButton(self.centralwidget)
        self.ledOnButton.setObjectName(u"ledOnButton")
        self.ledOnButton.setGeometry(QRect(250, 240, 81, 81))
        self.ledOnButton.clicked.connect(self.ledOn) # -> ledOn fonksiyonu çağrılıyor
       
        self.ledOffButton = QPushButton(self.centralwidget)
        self.ledOffButton.setObjectName(u"ledOffButton")
        self.ledOffButton.setGeometry(QRect(360, 240, 81, 81))
        self.ledOffButton.clicked.connect(self.ledOff) # -> ledOff fonksiyonu çağrılıyor
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 690, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MPU6050 GUI ile Veri Okuma", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"AccelX", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"AccelY", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"AccelZ", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"GyroX", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"GyroY", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"GyroZ", None))
        self.ledOnButton.setText(QCoreApplication.translate("MainWindow", u"ON", None))
        self.ledOffButton.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
    # retranslateUi
    
    # serial porttan veri okuma fonksiyonu
    def readData(self):
        time.sleep(0.1)
        read_data = esp32.readline().decode().split('\n')
        read_data = read_data[0].split(' ')
        print("DATA son hâli: " , read_data)
        return read_data
    
    # okunan veriyi yazdırma fonksiyonu
    def writeData(self, read_data):
        self.accelxLCD.display(float(read_data[0]))
        self.accelyLCD.display(float(read_data[1]))
        self.accelzLCD.display(float(read_data[2]))
        self.gyroxLCD.display(float(read_data[3]))
        self.gyroyLCD.display(float(read_data[4]))
        self.gyrozLCD.display(float(read_data[5]))
        
    def ledOn(self):
        esp32.write(b'1')
    
    def ledOff(self):
        esp32.write(b'0')
            
# portları listeleme -> mikrokontrolcünün bağlı olduğu portu bulma
# ports = list_ports.comports()
# for port in ports:
#     print(port)

# esp32 serial port bağlantısı
esp32 = serial.Serial("COM6", 115200)
print("Bağlı olan COM: " + esp32.name)


# veri okuma fonksiyonu
def read_and_update(ui):
    data = ui.readData()
    ui.writeData(data)
    
def main():
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    # sensör verisini güncellemek için timer
    timer = QTimer()
    timer.timeout.connect(lambda: read_and_update(ui))
    timer.start(1000)  # esp kodu gibi milisaniye delay(1000 ms = 1 saniye)
    
    read_and_update(ui)
    sys.exit(app.exec())
    
# uygulamayı başlatma               
if __name__ == "__main__":
    main()
    