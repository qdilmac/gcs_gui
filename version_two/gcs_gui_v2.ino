// Written by Mustafa Osman Dilmaç
// 30/05/2024 21:10

#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <math.h>

#define LED_one 25
#define LED_two 26
#define LED_three 27

class KalmanFilter {
  public:
    KalmanFilter() {
      Q_angle = 0.001;
      Q_bias = 0.003;
      R_measure = 0.03;

      angle = 0.0;
      bias = 0.0;

      P[0][0] = 0.0;
      P[0][1] = 0.0;
      P[1][0] = 0.0;
      P[1][1] = 0.0;
    }

    float getAngle(float newAngle, float newRate, float dt) {
      rate = newRate - bias;
      angle += dt * rate;

      P[0][0] += dt * (dt*P[1][1] - P[0][1] - P[1][0] + Q_angle);
      P[0][1] -= dt * P[1][1];
      P[1][0] -= dt * P[1][1];
      P[1][1] += Q_bias * dt;

      float S = P[0][0] + R_measure;
      float K[2];
      K[0] = P[0][0] / S;
      K[1] = P[1][0] / S;

      float y = newAngle - angle;

      angle += K[0] * y;
      bias += K[1] * y;

      float P00_temp = P[0][0];
      float P01_temp = P[0][1];

      P[0][0] -= K[0] * P00_temp;
      P[0][1] -= K[0] * P01_temp;
      P[1][0] -= K[1] * P00_temp;
      P[1][1] -= K[1] * P01_temp;

      return angle;
    }

  private:
    float Q_angle;
    float Q_bias;
    float R_measure;
    float angle;
    float bias;
    float rate;
    float P[2][2];
};

Adafruit_MPU6050 mpu;

// yaw verisi almak biraz sıkıntı ama olsun :d
float yaw = 0.0;
unsigned long lastUpdateTime = 0;

KalmanFilter kalmanRoll;
KalmanFilter kalmanPitch;
KalmanFilter kalmanYaw;

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
  delay(10);
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

  float filteredRoll = kalmanRoll.getAngle(roll, g.gyro.x, deltaTime);
  float filteredPitch = kalmanPitch.getAngle(pitch, g.gyro.y, deltaTime);
  float filteredYaw = kalmanYaw.getAngle(yaw, g.gyro.z, deltaTime);

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
  Serial.print(filteredRoll);  
  Serial.print(" ");
  Serial.print(filteredPitch);
  Serial.print(" ");
  Serial.print(filteredYaw);
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