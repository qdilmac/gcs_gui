# Version 2 of the camera/sensor data monitoring GUI
# @author: Mustafa Osman Dilmaç


from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, Signal, QThread, Slot)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QStatusBar, QWidget)
import sys
import serial
from serial.tools import list_ports
import time
import cv2
from ultralytics import YOLO
import torch
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1050, 720)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1050, 720))
        MainWindow.setMaximumSize(QSize(1050, 720))
        MainWindow.setStyleSheet(u"background-color: rgb(52, 57, 68);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.videofeed_label = QLabel(self.centralwidget)
        self.videofeed_label.setObjectName(u"videofeed_label")
        self.videofeed_label.setGeometry(QRect(40, 40, 640, 480))
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(690, 30, 321, 321))
        font = QFont()
        font.setBold(True)
        self.groupBox.setFont(font)
        self.gridLayoutWidget = QWidget(self.groupBox)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 30, 301, 281))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)

        self.line_5 = QFrame(self.gridLayoutWidget)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_5, 8, 0, 1, 1)

        self.line_4 = QFrame(self.gridLayoutWidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_4, 6, 0, 1, 1)

        self.line_7 = QFrame(self.gridLayoutWidget)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.HLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_7, 12, 0, 1, 1)

        self.gyrox_label = QLabel(self.gridLayoutWidget)
        self.gyrox_label.setObjectName(u"gyrox_label")

        self.gridLayout_2.addWidget(self.gyrox_label, 7, 1, 1, 1)

        self.rollangle_label = QLabel(self.gridLayoutWidget)
        self.rollangle_label.setObjectName(u"rollangle_label")

        self.gridLayout_2.addWidget(self.rollangle_label, 13, 1, 1, 1)

        self.line_2 = QFrame(self.gridLayoutWidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_2, 2, 1, 1, 1)

        self.accelz_label = QLabel(self.gridLayoutWidget)
        self.accelz_label.setObjectName(u"accelz_label")

        self.gridLayout_2.addWidget(self.accelz_label, 5, 1, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.gridLayout_2.addWidget(self.label_3, 13, 0, 1, 1)

        self.label_10 = QLabel(self.gridLayoutWidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.gridLayout_2.addWidget(self.label_10, 9, 0, 1, 1)

        self.line = QFrame(self.gridLayoutWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line, 2, 0, 1, 1)

        self.accelx_label = QLabel(self.gridLayoutWidget)
        self.accelx_label.setObjectName(u"accelx_label")

        self.gridLayout_2.addWidget(self.accelx_label, 1, 1, 1, 1)

        self.gyroz_label = QLabel(self.gridLayoutWidget)
        self.gyroz_label.setObjectName(u"gyroz_label")

        self.gridLayout_2.addWidget(self.gyroz_label, 11, 1, 1, 1)

        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.gridLayout_2.addWidget(self.label_5, 15, 0, 1, 1)

        self.accely_label = QLabel(self.gridLayoutWidget)
        self.accely_label.setObjectName(u"accely_label")

        self.gridLayout_2.addWidget(self.accely_label, 3, 1, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.line_6 = QFrame(self.gridLayoutWidget)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_6, 10, 0, 1, 1)

        self.label_6 = QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.gridLayout_2.addWidget(self.label_6, 5, 0, 1, 1)

        self.label_12 = QLabel(self.gridLayoutWidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)

        self.gridLayout_2.addWidget(self.label_12, 11, 0, 1, 1)

        self.line_3 = QFrame(self.gridLayoutWidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_3, 4, 0, 1, 1)

        self.label_7 = QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.gridLayout_2.addWidget(self.label_7, 7, 0, 1, 1)

        self.pitchangle_label = QLabel(self.gridLayoutWidget)
        self.pitchangle_label.setObjectName(u"pitchangle_label")

        self.gridLayout_2.addWidget(self.pitchangle_label, 15, 1, 1, 1)

        self.gyroy_label = QLabel(self.gridLayoutWidget)
        self.gyroy_label.setObjectName(u"gyroy_label")

        self.gridLayout_2.addWidget(self.gyroy_label, 9, 1, 1, 1)

        self.line_8 = QFrame(self.gridLayoutWidget)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.HLine)
        self.line_8.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_8, 14, 0, 1, 1)

        self.line_9 = QFrame(self.gridLayoutWidget)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShape(QFrame.HLine)
        self.line_9.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_9, 14, 1, 1, 1)

        self.line_10 = QFrame(self.gridLayoutWidget)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setFrameShape(QFrame.HLine)
        self.line_10.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_10, 12, 1, 1, 1)

        self.line_11 = QFrame(self.gridLayoutWidget)
        self.line_11.setObjectName(u"line_11")
        self.line_11.setFrameShape(QFrame.HLine)
        self.line_11.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_11, 10, 1, 1, 1)

        self.line_12 = QFrame(self.gridLayoutWidget)
        self.line_12.setObjectName(u"line_12")
        self.line_12.setFrameShape(QFrame.HLine)
        self.line_12.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_12, 8, 1, 1, 1)

        self.line_13 = QFrame(self.gridLayoutWidget)
        self.line_13.setObjectName(u"line_13")
        self.line_13.setFrameShape(QFrame.HLine)
        self.line_13.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_13, 6, 1, 1, 1)

        self.line_14 = QFrame(self.gridLayoutWidget)
        self.line_14.setObjectName(u"line_14")
        self.line_14.setFrameShape(QFrame.HLine)
        self.line_14.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_14, 4, 1, 1, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(690, 360, 321, 161))
        self.groupBox_2.setFont(font)
        self.gridLayoutWidget_2 = QWidget(self.groupBox_2)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(10, 20, 301, 131))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.led2_button = QPushButton(self.gridLayoutWidget_2)
        self.led2_button.setObjectName(u"led2_button")
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.led2_button.setFont(font1)

        self.gridLayout_3.addWidget(self.led2_button, 2, 0, 1, 1)

        self.led1_button = QPushButton(self.gridLayoutWidget_2)
        self.led1_button.setObjectName(u"led1_button")
        self.led1_button.setFont(font1)

        self.gridLayout_3.addWidget(self.led1_button, 1, 0, 1, 1)

        self.led3_button = QPushButton(self.gridLayoutWidget_2)
        self.led3_button.setObjectName(u"led3_button")
        self.led3_button.setFont(font1)

        self.gridLayout_3.addWidget(self.led3_button, 3, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(30, 530, 651, 161))
        self.groupBox_3.setFont(font)
        self.gridLayoutWidget_3 = QWidget(self.groupBox_3)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(10, 20, 631, 131))
        self.gridLayout_4 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.camerastop_button = QPushButton(self.gridLayoutWidget_3)
        self.camerastop_button.setObjectName(u"camerastop_button")
        self.camerastop_button.setFont(font1)

        self.gridLayout_6.addWidget(self.camerastop_button, 2, 0, 1, 1)

        self.camerastart_button_face = QPushButton(self.gridLayoutWidget_3)
        self.camerastart_button_face.setObjectName(u"camerastart_button_face")
        self.camerastart_button_face.setFont(font1)

        self.gridLayout_6.addWidget(self.camerastart_button_face, 0, 0, 1, 1)

        self.camerastart_button_object = QPushButton(self.gridLayoutWidget_3)
        self.camerastart_button_object.setObjectName(u"camerastart_button_object")
        self.camerastart_button_object.setFont(font1)

        self.gridLayout_6.addWidget(self.camerastart_button_object, 1, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_6, 0, 3, 1, 1)

        self.line_15 = QFrame(self.gridLayoutWidget_3)
        self.line_15.setObjectName(u"line_15")
        self.line_15.setFrameShape(QFrame.VLine)
        self.line_15.setFrameShadow(QFrame.Sunken)

        self.gridLayout_4.addWidget(self.line_15, 0, 1, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.datastart_button = QPushButton(self.gridLayoutWidget_3)
        self.datastart_button.setObjectName(u"datastart_button")
        self.datastart_button.setFont(font1)

        self.gridLayout_5.addWidget(self.datastart_button, 0, 0, 1, 1)

        self.datastop_button = QPushButton(self.gridLayoutWidget_3)
        self.datastop_button.setObjectName(u"datastop_button")
        self.datastop_button.setFont(font1)

        self.gridLayout_5.addWidget(self.datastop_button, 1, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_5, 0, 0, 1, 1)

        self.line_16 = QFrame(self.gridLayoutWidget_3)
        self.line_16.setObjectName(u"line_16")
        self.line_16.setFrameShape(QFrame.VLine)
        self.line_16.setFrameShadow(QFrame.Sunken)

        self.gridLayout_4.addWidget(self.line_16, 0, 2, 1, 1)

        self.detection_label = QLabel(self.centralwidget)
        self.detection_label.setObjectName(u"detection_label")
        self.detection_label.setGeometry(QRect(80, 40, 551, 41))
        font2 = QFont()
        font2.setPointSize(15)
        font2.setBold(True)
        self.detection_label.setFont(font2)
        self.detection_label.setFrameShape(QFrame.Box)
        self.detection_label.setFrameShadow(QFrame.Sunken)
        self.detection_label.setLineWidth(2)
        self.detection_label.setMidLineWidth(2)
        self.detection_label.setAlignment(Qt.AlignCenter)
        self.detection_label.setWordWrap(False)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
        
        self.CameraThread = Camera_Worker() # -> camera thread oluşturuluyor
        self.CameraThread.ImageUpdate.connect(self.ImageUpdateSlot) # -> camera thread içerisindeki ImageUpdate sinyali ImageUpdateSlot fonksiyonuna bağlanıyor
        self.CameraThread.FacesDetected.connect(self.update_detection_label_face) # -> yüz tespiti sinyali detection_label'ı güncellemek için kullanılacak
        self.camerastart_button_face.clicked.connect(self.start_camera_face) # -> yüz tespiti için kamera başlatma butonuna bağlanıyor
        #queued connection ile thread içerisinde çalışan fonksiyonun bitmesini bekliyoruz. Bu detecion_label'ı güncellemede işe yaradı ama hala videofeed_label'da bir frame daha geliyor.

        self.CameraObjectThread = Camera_Object_Worker() # -> obje tespiti için camera thread oluşturuluyor
        self.CameraObjectThread.ImageUpdate.connect(self.ImageUpdateSlot) # -> camera thread içerisindeki ImageUpdate sinyali ImageUpdateSlot fonksiyonuna bağlanıyor
        self.CameraObjectThread.ObjectsDetected.connect(self.update_detection_label_object) # -> obje tespiti sinyali detection_label'ı güncellemek için kullanılacak
        self.camerastart_button_object.clicked.connect(self.start_camera_object) # -> obje tespiti için kamera başlatma butonuna bağlanıyor
        
        self.camerastop_button.clicked.connect(self.stop_camera, Qt.QueuedConnection) # -> stop_camera fonksiyonu thread içerisinde çalıştığı için queued connection kullanıyoruz
    
    def start_camera_face(self):
        self.CameraObjectThread.stop() # -> obje tespiti thread'ini durdur
        # time.sleep(1) # -> thread'in bitmesini beklemek için 1 saniye bekle
        self.CameraThread.start()
        self.camerastart_button_face.setStyleSheet("background-color: green;")
        self.camerastart_button_object.setStyleSheet("background-color: #343944;")
        self.camerastop_button.setStyleSheet("background-color: #343944;") # -> ana pencerenin renk hex kodu
        self.CameraThread.FacesDetected.connect(self.update_detection_label_face)
        
    def start_camera_object(self):
        self.CameraThread.stop() # -> yüz tespiti thread'ini durdur
        # time.sleep(1) # -> yüz tespiti thread'inin bitmesini beklemek için 1 saniye bekletme
        self.CameraObjectThread.start()
        self.camerastart_button_object.setStyleSheet("background-color: green;")
        self.camerastart_button_face.setStyleSheet("background-color: #343944;")
        self.camerastop_button.setStyleSheet("background-color: #343944;")
        self.CameraObjectThread.ObjectsDetected.connect(self.update_detection_label_object)

    def stop_camera(self):
        self.camerastart_button_face.setStyleSheet("background-color: #343944;")
        self.camerastart_button_object.setStyleSheet("background-color: #343944;")
        self.camerastop_button.setStyleSheet("background-color: red;")
        self.detection_label.setText("IDLE")  # detection_label'ı değiştir
        self.detection_label.setStyleSheet("background-color: orange;")
        self.videofeed_label.clear() # -> videofeed_label temizlemesi gerek ama temizledikten sonra geriye bir frame daha geliyor. Tekrar butona basılması gerekiyor.
       
        self.CameraThread.FacesDetected.disconnect(self.update_detection_label_face) # -> yüz tespiti sinyalini disconnect et
        self.CameraThread.stop()
        self.CameraThread.wait() # -> thread'in bitmesini bekliyoruz -> çift tıklama sorununu bu da çözmedi :d
       
        self.CameraObjectThread.ObjectsDetected.disconnect(self.update_detection_label_object) # -> obje tespiti sinyalini disconnect et 
        self.CameraObjectThread.stop()
        self.CameraObjectThread.wait()
   
    @Slot (int) # -> yüz tespiti sinyali veri tipini belirtiyoruz, çift dikiş daha sağlam olsun diye
    def update_detection_label_face(self, detected_faces: int):
        if detected_faces >= 1:
            self.detection_label.setText(f"{detected_faces} adet Yüz Tespit Edildi")
            self.detection_label.setStyleSheet("background-color: green;")
        else:
            self.detection_label.setText("Yüz Tespiti Yapılamadı!")
            self.detection_label.setStyleSheet("background-color: red;")
    
    @Slot (int)
    def update_detection_label_object(self, detected_objects):
        if detected_objects >= 1:
            self.detection_label.setText(f"{detected_objects} adet Obje Tespit Edildi")
            self.detection_label.setStyleSheet("background-color: green;")
        else:
            self.detection_label.setText("Obje Tespiti Yapılamadı!")
            self.detection_label.setStyleSheet("background-color: red;")
    
    @Slot (QImage)
    def ImageUpdateSlot(self, image): # -> ImageUpdate sinyali ile gelen resmi VideoFeedLabel'a set ediyor
        self.videofeed_label.setPixmap(QPixmap.fromImage(image)) 
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Data Monitoring GUI v0.2", None))
        self.videofeed_label.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Sensor Data - READ", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"AccelY", None))
        self.gyrox_label.setText("")
        self.rollangle_label.setText("")
        self.accelz_label.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Roll Angle", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"GyroY", None))
        self.accelx_label.setText("")
        self.gyroz_label.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Pitch Angle", None))
        self.accely_label.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"AccelX", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"AccelZ", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"GyroZ", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"GyroX", None))
        self.pitchangle_label.setText("")
        self.gyroy_label.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Sensor Data - WRITE", None))
        self.led2_button.setText(QCoreApplication.translate("MainWindow", u"Led 2", None))
        self.led1_button.setText(QCoreApplication.translate("MainWindow", u"Led 1", None))
        self.led3_button.setText(QCoreApplication.translate("MainWindow", u"Led 3", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Connections", None))
        self.camerastop_button.setText(QCoreApplication.translate("MainWindow", u"Stop Camera Feed", None))
        self.camerastart_button_face.setText(QCoreApplication.translate("MainWindow", u"Start Camera Feed - Face Detection", None))
        self.camerastart_button_object.setText(QCoreApplication.translate("MainWindow", u"Start Camera Feed - Object Detection", None))
        self.datastart_button.setText(QCoreApplication.translate("MainWindow", u"Start Data Reading", None))
        self.datastop_button.setText(QCoreApplication.translate("MainWindow", u"Stop Data Reading", None))
        self.detection_label.setText("")
    # retranslateUi

# Camera Thread
class Camera_Worker(QThread):
    ImageUpdate = Signal(QImage) # -> the tutorial I watched used pyqtSignal but I guess its changed
    FacesDetected = Signal(int) # -> yüz tespiti sinyali, detection_label'ı güncellemek için kullanılacak
    
    # OPENCV ile Yüz Tespiti
    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') # -> yüz tespiti için haarcascade dosyası
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)) # -> yüz tespiti
                detected_faces = len(faces)
                self.FacesDetected.emit(detected_faces) # -> yüz tespiti sinyali
                for (x, y, w, h) in faces: # -> yüzün etrafına dikdörtgen çizme
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) # -> dikdörtgenin rengi ve kalınlığı
                    # Çizilen dikdörtgenin merkezini hesaplama
                    center_x = x + w // 2
                    center_y = y + h // 2
                    # Bulunan merkezi bounding boxun üstüne yazdırma
                    cv2.putText(frame, f"({center_x}, {center_y})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                RGBImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # FlippedImage = cv2.flip(RGBImage, 1)
                ConvertToQtFormat = QImage(RGBImage.data, RGBImage.shape[1], RGBImage.shape[0], QImage.Format_RGB888)
                # yukarıdaki satırda RGBImage yerine FlippedImage yazarak görüntüyü ters çevirebiliriz.
                # bu işlem gerçek hayattaki hareket yönüne göre gördüğümüz kamera verisini ayarlamamızı sağlıyor.
                # ben şimdilik ters çevirmeden RGBImage kullanıyorum. Üstüne yazdığım metinler ters olmasın diye.
                
                pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(pic)
                
    def stop(self):
        self.ThreadActive = False
        self.quit()
        self.wait()

class Camera_Object_Worker(QThread):
    ImageUpdate = Signal(QImage)
    ObjectsDetected = Signal(int)
    
    # Kendi Eğittiğim YOLO modeli ile Obje Tespiti
    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        
        model_path = 'C:/Users/shade/OneDrive/Masaüstü/software docs/mpu6050_pyqt/version_two/best.pt'  # Update this path to your weight file
        if not os.path.exists(model_path):
            print(f"Model file not found at {model_path}")
            return

        # -> YOLO modelini yükleme
        model = YOLO(model_path)

        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                # -> YOLO modelini kullanarak obje tespiti
                results = model(frame)
                detected_objects = 0
                
                # -> YOLO modelinden gelen sonuçları işleme
                for result in results:
                    labels = model.names  # -> YOLO modelinden gelen label'ları al
                    for box in result.boxes:
                        if int(box.cls[0]) == 0:  # -> Assuming class 0 is for object
                            detected_objects += 1
                            x1, y1, x2, y2 = map(int, box.xyxy[0])  # -> Bounding box kooridinatlarını al
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # -> Bounding box çiz
                            
                            # Get the class label and confidence
                            class_id = int(box.cls[0])
                            label = labels[class_id]
                            confidence = box.conf[0]

                            # -> YOLO model Label'ı bounding boxun üstüne yazdır
                            cv2.putText(frame, f"{label}: {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                self.ObjectsDetected.emit(detected_objects)  # -> Obje tespiti sinyali
                
                RGBImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                ConvertToQtFormat = QImage(RGBImage.data, RGBImage.shape[1], RGBImage.shape[0], QImage.Format_RGB888)
                
                pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(pic)
                
    def stop(self):
        self.ThreadActive = False
        self.quit()
        self.wait()

def main():
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
    
# uygulamayı başlatma
if __name__ == "__main__":
    main()