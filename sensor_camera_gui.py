# Author: Mustafa Osman Dilmaç
# Simple PYQT6 GUI to monitor sensor data from ESP32 and camera feed from webcam

# -*- coding: utf-8 -*-

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QThread, Signal, QTimer)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLCDNumber,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QStatusBar, QWidget)
from PySide6 import QtWidgets
import time
import serial
from serial.tools import list_ports
import sys
import cv2

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(960, 720)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(960, 720))
        MainWindow.setMaximumSize(QSize(960, 720))
        font = QFont()
        font.setBold(False)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.accelxLCD = QLCDNumber(self.centralwidget)
        self.accelxLCD.setObjectName(u"accelxLCD")
        self.accelxLCD.setGeometry(QRect(240, 400, 151, 41))
        self.accelyLCD = QLCDNumber(self.centralwidget)
        self.accelyLCD.setObjectName(u"accelyLCD")
        self.accelyLCD.setGeometry(QRect(240, 450, 151, 41))
        self.accelzLCD = QLCDNumber(self.centralwidget)
        self.accelzLCD.setObjectName(u"accelzLCD")
        self.accelzLCD.setGeometry(QRect(240, 500, 151, 41))
        self.gyrozLCD = QLCDNumber(self.centralwidget)
        self.gyrozLCD.setObjectName(u"gyrozLCD")
        self.gyrozLCD.setGeometry(QRect(560, 500, 151, 41))
        self.gyroxLCD = QLCDNumber(self.centralwidget)
        self.gyroxLCD.setObjectName(u"gyroxLCD")
        self.gyroxLCD.setGeometry(QRect(560, 400, 151, 41))
        self.gyroyLCD = QLCDNumber(self.centralwidget)
        self.gyroyLCD.setObjectName(u"gyroyLCD")
        self.gyroyLCD.setGeometry(QRect(560, 450, 151, 41))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(190, 410, 49, 16))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(190, 460, 49, 16))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(190, 510, 49, 16))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(510, 410, 49, 16))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(510, 460, 49, 16))
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(510, 510, 49, 16))
        self.VideoFeedLabel = QLabel(self.centralwidget)
        self.VideoFeedLabel.setObjectName(u"VideoFeedLabel")
        self.VideoFeedLabel.setGeometry(QRect(30, 20, 891, 331))
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(350, 560, 221, 111))
        self.horizontalLayoutWidget = QWidget(self.groupBox)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(30, 20, 160, 80))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        
        self.ledOnButton = QPushButton(self.horizontalLayoutWidget)
        self.ledOnButton.setObjectName(u"ledOnButton")
        self.ledOnButton.clicked.connect(self.ledOn) # -> ledOn fonksiyonu çağrılıyor
        self.horizontalLayout.addWidget(self.ledOnButton)

        self.ledOffButton = QPushButton(self.horizontalLayoutWidget)
        self.ledOffButton.setObjectName(u"ledOffButton")
        self.ledOffButton.clicked.connect(self.ledOff)
        self.horizontalLayout.addWidget(self.ledOffButton) # -> ledOff fonksiyonu çağrılıyor

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(0, 0, 961, 20))
        font1 = QFont()
        font1.setBold(True)
        self.label_8.setFont(font1)
        self.label_8.setAlignment(Qt.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
        
        self.CameraThread = Camera_Worker() # -> camera thread oluşturuluyor
        self.CameraThread.ImageUpdate.connect(self.ImageUpdateSlot) # -> camera thread içerisindeki ImageUpdate sinyali ImageUpdateSlot fonksiyonuna bağlanıyor
        self.CameraThread.start() # -> camera thread başlatılıyor
        
        self.DataThread = Data_Worker() # -> data thread oluşturuluyor
        self.DataThread.DataUpdate.connect(self.DataUpdateSlot) # -> data thread içerisindeki DataUpdate sinyali DataUpdateSlot fonksiyonuna bağlanıyor
        self.DataThread.start() # -> data thread başlatılıyor
        
    def ImageUpdateSlot(self, image): # -> ImageUpdate sinyali ile gelen resmi VideoFeedLabel'a set ediyor
        self.VideoFeedLabel.setPixmap(QPixmap.fromImage(image)) 
        
    def DataUpdateSlot(self, data): # -> DataUpdate sinyali ile gelen veriyi LCD'lere yazdırıyor
        self.accelxLCD.display(float(data[0]))
        self.accelyLCD.display(float(data[1]))
        self.accelzLCD.display(float(data[2]))
        self.gyroxLCD.display(float(data[3]))
        self.gyroyLCD.display(float(data[4]))
        self.gyrozLCD.display(float(data[5]))
        
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Sensor/Camera Data Monitoring v0.1", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"AccelX", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"AccelY", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"AccelZ", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"GyroX", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"GyroY", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"GyroZ", None))
        self.VideoFeedLabel.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Led Control", None))
        self.ledOnButton.setText(QCoreApplication.translate("MainWindow", u"ON", None))
        self.ledOffButton.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label_8.setStyleSheet(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Video Feed", None))
    # retranslateUi
       
    def ledOn(self):
        esp32.write(b'1')
        print("LED ON")
    
    def ledOff(self):
        esp32.write(b'0')
        print("LED OFF")
            
# portları listeleme -> mikrokontrolcünün bağlı olduğu portu bulma
# ports = list_ports.comports()
# for port in ports:
#     print(port)

# esp32 serial port bağlantısını sağlama, şimdilik Hardcoded
esp32 = serial.Serial("COM6", 115200)
print("Bağlı olan COM: " + esp32.name)
    
# Camera Thread
class Camera_Worker(QThread):
    ImageUpdate = Signal(QImage) # -> the tutorial I watched used pyqtSignal but I guess its changed
    
    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                RGBImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(RGBImage, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio) # -> 891, 331 video feed label boyutları, ama burada 640x480 verdim sorun yok
                self.ImageUpdate.emit(pic) # -> ImageUpdate sinyali işlenmiş resmi ImageUpdateSlot fonksiyonuna gönderiyor (emit ediyor)
    
    def stop(self):
        self.ThreadActive = False
        self.quit()

# Data Thread
class Data_Worker(QThread):
    DataUpdate = Signal(list)
    
    # serial porttan veri okuma fonksiyonu
    def readData(self):
        time.sleep(0.1)
        read_data = esp32.readline().decode().split('\n')
        read_data = read_data[0].split(' ')
        print("DATA son hâli: " , read_data)
        return read_data
    
    # okunan veriyi yazdırma fonksiyonu
    # def writeData(self, read_data):
    #     self.accelxLCD.display(float(read_data[0]))
    #     self.accelyLCD.display(float(read_data[1]))
    #     self.accelzLCD.display(float(read_data[2]))
    #     self.gyroxLCD.display(float(read_data[3]))
    #     self.gyroyLCD.display(float(read_data[4]))
    #     self.gyrozLCD.display(float(read_data[5]))
        
    #     # veri okuma fonksiyonu
    # def read_and_update(ui):
    #     data = ui.readData()
    #     ui.writeData(data)

    def run(self):
        self.ThreadActive = True
        while self.ThreadActive:
            data = Data_Worker.readData(self)
            self.DataUpdate.emit(data) # -> DataUpdate sinyali işlenmiş veriyi DataUpdateSlot fonksiyonuna gönderiyor (emit ediyor)
            
    def stop(self):
        self.ThreadActive = False
        self.quit()

def main():
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    # # sensör verisini güncellemek için timer
    # timer = QTimer()
    # timer.timeout.connect(lambda: read_and_update(ui))
    # timer.start(1000)  # esp kodu gibi milisaniye delay(1000 ms = 1 saniye)
    # read_and_update(ui)
    
    sys.exit(app.exec())
    
# uygulamayı başlatma
if __name__ == "__main__":
    main()
    