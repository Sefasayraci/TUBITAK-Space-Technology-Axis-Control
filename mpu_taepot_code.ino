#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  mpu.initialize();
}

void loop() {
  int ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);

  float roll = atan2(ay, az) * 180.0 / PI;
  float pitch = atan2(-ax, sqrt(ay * ay + az * az)) * 180.0 / PI;

  Serial.print(roll);
  Serial.print("/");
  Serial.println(pitch);

  delay(100);
}
