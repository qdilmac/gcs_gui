// Written by Mustafa Osman Dilmaç
// 30/05/2024 21:10

#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <math.h>

#define LED_one 25
#define LED_two 26
#define LED_three 27

Adafruit_MPU6050 mpu;

// yaw verisi almak biraz sıkıntı ama olsun :d
float yaw = 0.0;
unsigned long lastUpdateTime = 0;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1000);
  while (!Serial) {
    delay(10);
  }

  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }

  pinMode(LED_one, OUTPUT);
  pinMode(LED_two, OUTPUT);
  pinMode(LED_three, OUTPUT);

  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.println("");
  delay(100);
}

void loop() {
  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Yatış (roll), Yunuslama (pitch), Sapma (Yaw) hesaplamaları
  float roll = atan2(a.acceleration.y, a.acceleration.z) * 180 / PI;
  float pitch = atan2(-a.acceleration.x, sqrt(a.acceleration.y * a.acceleration.y + a.acceleration.z * a.acceleration.z)) * 180 / PI;

  // Geçen zaman hesabı -> bu yüzden yaw hesabı biraz sıkıntılı
  unsigned long currentTime = millis();
  float deltaTime = (currentTime - lastUpdateTime) / 1000.0; // milisaniye -> saniye
  lastUpdateTime = currentTime;

  yaw += g.gyro.z * deltaTime;
  yaw = fmod(yaw, 360.0); // Veri sapması 360 dereceden büyük olmamalı -> Roll-Yaw-Pitch hesaplamalarına kalman filtresi eklenecek

  /* Print out the values */
  Serial.print(a.acceleration.x);
  Serial.print(" ");
  Serial.print(a.acceleration.y);
  Serial.print(" ");
  Serial.print(a.acceleration.z);
  Serial.print(" ");
  Serial.print(g.gyro.x);
  Serial.print(" ");
  Serial.print(g.gyro.y);
  Serial.print(" ");
  Serial.print(g.gyro.z);
  Serial.print(" ");
  // mpu6050 sensörünün eksenel yönlerine göre veriyi gönderiyorum
  Serial.print(roll);  
  Serial.print(" ");
  Serial.print(pitch);
  Serial.print(" ");
  Serial.print(yaw);
  Serial.println();
  delay(300);

  // LED kontrol serial port üzerinden
  if (Serial.available() > 0) {
    char command = Serial.read();
    switch (command) {
      case '1':
        digitalWrite(LED_one, HIGH);
        break;
      case '2':
        digitalWrite(LED_one, LOW);
        break;
      case '3':
        digitalWrite(LED_two, HIGH);
        break;
      case '4':
        digitalWrite(LED_two, LOW);
        break;
      case '5':
        digitalWrite(LED_three, HIGH);
        break;
      case '6':
        digitalWrite(LED_three, LOW);
        break;
      default:
        // Unknown command
        break;
    }
  }
}
