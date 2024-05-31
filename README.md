# Monitoring Sensor Data / Camera Feed GUI with Pyside

## Description
Main reason of this project is to learn by doing aka "Project Based Learning". This is a graphical user interface (GUI) designed for monitoring camera and sensor data. Developed using PySide6 for the GUI elements, it integrates with camera feeds for face and object detection and displays sensor data from MPU6050 (more sensors can be added ofc). The GUI provides a user-friendly interface for starting and stopping camera feeds, controlling LEDs, and viewing real-time sensor data. Project includes different versions that shows my progress about the topic(s).

I first wrote this project to create a simple Pyside GUI and read data from an MPU6050 sensor connected to an ESP32 microcontroller. The sensor data (accelerometer and gyroscope readings) are displayed on the GUI's designated LCD displays. This was a small "unknown" for me but I'm happy that I solved the problem. It took some time but I managed it in couple hours. If this helps you out in any way, feel free to use it!

Update 26/05 -> The project took a different route that I have expected but I'm not complaining. The GCS concept is one of the main parts of my robotics (UGV, UAV, Robotic Arm etc.) projects. So every second that i spent on this is worth the time!

## Updates
14/05/2024 -> Added simple led to the circuit to not only read but also send serial data to control components. Will be useful in future for remote control applications.

18/05/2024 -> Added camera feed with multithreading. The project changed course and now it started to resemble a complete gui with camera feed, sensor data monitoring and sending data over serial.

19/05/2024 -> Added another thread for data monitoring. This solved stuttering in camera feed.

20/05/2024 -> Added face detection.

26/05/2024 -> Organized the repo into folders for different versions. Started working on second version.

27/05/2024 -> Trained my first custom YOLOv8 object detection model with my own dataset to implement it to the GUI. Added another thread to seperate face and object detection.

27/05/2024 22:56 -> Trained another model with Turkish 1 lira coin. Training went well but it does not work good in poor light. And accidentally named the coin class wrong as a "thermos". Forgot to change it from the model before :D

30/05/2024 -> Added serial read and serial write functionality to the version 2 of the GUI.

## TO-DO
Test or implement communication over a network. Eliminate the need for wired serial connection. -> <b>WIP</b>

Add face detection to test processed image monitoring -> <b>DONE</b>

Train a YOLO model and implement it. Add it as a different thread so when camera starts I can both track face or trained object. -> <b>DONE, This was so useful and educational!</b>

Add angle estimation using Kalman filtering. -> <b>Added angle est., Kalman WIP </b>

Update GUI for v2-> <b>DONE</b>

## Problems
To use camera feed without 1 second pauses I need to find efficient way to read data without stopping camera feed every second. I might be able to use another thread for it. -> <b>SOLVED, implementing another thread works</b>

"TypeError: '>=' not supported between instances of 'PySide6.QtGui.QImage' and 'int'". Even tho the type of FaceDetection signal is integer, this error occurs. But program works well without any problem. -> <b>SOLVED, it appears in some places I wrote ImageUpdate signal instead of FaceDetection signal *facepalm* </b> 

I have to click twice to the "Stop Camera Feed" button to clear videofeed_label and update "detection_label". Same happens on data reading. I think its something about threads not stopping immediately when I click the button. -> <b>UNSOLVED</b>

When I start object detection after stopping the camera feed the detection_label does not update. Same problem does not happen when i start face detection. -> <b>SOLVED</b>

![image](https://github.com/qdilmac/gcs_gui/assets/64690728/3df430d1-d97c-473a-bb93-f60ecb704670) -> 30 min test by letting the sensor stand still on table. Sensor reading drift. Will be solved when KF implemented -> <b>UNSOLVED</b>
  - ![image](https://github.com/qdilmac/gcs_gui/assets/64690728/ea14ab3b-dada-427b-a9a3-3c2886f4290b) -> first iteration of KF, same test results



## Requirements
- Python 3
- PyQT / Pyside
- pySerial
- QTDesigner (easier UI design)
- MPU6050
- ESP32s
