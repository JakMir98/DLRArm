#include <Servo.h>
#define SIZE 6

byte buff[SIZE];
Servo servo1;
int angle1 = 90;
Servo servo2;
int angle2 = 90;
Servo servo3;
int angle3 = 90;
Servo servo4;
int angle4 = 90;
Servo servo5;
int angle5 = 90;
Servo servo6;
int angle6 = 90;

void setup() {
  Serial.begin(9600);
  
  servo1.attach(4);
  servo2.attach(5);
  servo3.attach(6);
  servo4.attach(7);
  servo5.attach(8);
  servo6.attach(9);
}

void loop() {
  while (Serial.read() != 200){
  }
  
  delay(50);
  if (Serial.readBytes(buff, SIZE) == SIZE) {
    angle1 = buff[0];
    angle2 = buff[1];
    angle3 = buff[2];
    angle4 = buff[3];
    angle5 = buff[4];
    angle6 = buff[5];
    
    //Serial.println(angle1);
    //Serial.println(angle2);
    //Serial.println(angle3);
    //Serial.println(angle4);
    //Serial.println(angle5);
    //Serial.println(angle6);

    servo1.write(angle1);
    servo2.write(angle2);
    servo3.write(angle3);
    servo4.write(angle4);
    servo5.write(angle5);
    servo6.write(angle6);

    delay(50);
  }
}
