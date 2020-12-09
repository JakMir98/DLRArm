#include <Servo.h>
#define SIZE 6
#define WAIT_FOR_SERVO 50

byte buff[SIZE] = {0x5A, 0x5A, 0x5A, 0x5A, 0x5A, 0x5A};
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;


void move(byte buff[SIZE]) {
    int angle1 = buff[0];
    int angle2 = buff[1];
    int angle3 = buff[2];
    int angle4 = buff[3];
    int angle5 = buff[4];
    int angle6 = buff[5];
    
    Serial.println(angle1);  // for debugging purposes
    Serial.println(angle2);
    Serial.println(angle3);
    Serial.println(angle4);
    Serial.println(angle5);
    Serial.println(angle6);

    servo1.write(angle1);
    delay(WAIT_FOR_SERVO);
    
    servo2.write(angle2);
    delay(WAIT_FOR_SERVO);
    
    servo3.write(angle3);
    delay(WAIT_FOR_SERVO);
    
    servo4.write(angle4);
    delay(WAIT_FOR_SERVO);
    
    servo5.write(angle5);
    delay(WAIT_FOR_SERVO);
    
    servo6.write(angle6);
    delay(WAIT_FOR_SERVO);
}

void setup() {
  Serial.begin(9600);
  
  servo1.attach(4);
  servo2.attach(5);
  servo3.attach(6);
  servo4.attach(7);
  servo5.attach(8);
  servo6.attach(9);
  
  move(buff);                                   // move to the neutral position
}

void loop() {
  while (Serial.read() != 200){
  }                                             // wait for indicator
  
  //Serial.println(201); // for debugging purposes
  delay(10);                                    // wait for serial buffer to fill up
  
  if (Serial.readBytes(buff, SIZE) == SIZE) {  
    move(buff);
  }                                             // move if successfully read SIZE positions
}
