#include <Servo.h>

Servo servo1;        // Left / Right
Servo servo2;        // Up / Down

static int v1 = 90;   // Head Left/Right starting position
static int v2 = 105;  // Skull up/down starting position (90 is straight up/down)
static int vel = 2;   // Turning velocity

long counter = 0;      // For counting...
int moveDir = -1;

void setup() {
  
  pinMode(1,OUTPUT);
  servo1.attach(9); //analog pin 0 - left/right
  //servo1.setMaximumPulse(2000);
  //servo1.setMinimumPulse(700);
  servo2.attach(11); //analog pin 1 - up/down
  
  servo1.write(v1);  // Move to starting position
  servo2.write(v2);
  
  Serial.begin(9600);
  Serial.println("Ready");

}

void loop() {
  
  if ( Serial.available() ) {
    char ch = Serial.read();
    
    switch(ch) {
      //case '0'...'9':
      //  vel = ch;
      //  break;
      case 'D':
        servo2.write(servo2.read() - vel);
        // this was 15
        //delay(5);
        break;
      case 'U':
        servo2.write(servo2.read() + vel);
        //delay(5);
        break;
      case 'R':
        servo1.write(servo1.read() + vel);
        //delay(5);
        break;
      case 'L':
        servo1.write(servo1.read() - vel);
        //delay(5);
        break;;
      case 'X':
        break;
    }
    
    counter = 1000000;    // reset counter
    
  } else {
    // count a bit, then call 'lost_face'
    if (counter == 0) {
      lostFace();
    } else {
      counter -= 1;
    }
  }
}

void lostFace() {
  servo2.write(v2);
  delay(15);
  
  int curPos = servo1.read();
  
  if (curPos >= 180) {
    moveDir = -1;
  } else if (curPos <= 0) {
    moveDir = 1;
  }
  
  servo1.write(curPos + (moveDir * vel));
  delay(50);
}
