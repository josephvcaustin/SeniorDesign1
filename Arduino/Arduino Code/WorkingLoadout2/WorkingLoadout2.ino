
#include <QTRSensors.h>
#include <Servo.h>

#define NUM_SENSORS 16
#define kp  10
#define ki  0.001
#define kd  30
#define MID_VAL 7500
#define MID_ANGLE 103
#define SERVO  10
#define ESC  9
#define LEFT 135
#define RIGHT 75
#define LED 7
#define STOP 1350
#define GO 1410
#define FAST 1430
#define SLOW 1390
#define NORMALIZE 20

Servo turn;
Servo esc;

// create an object for 16 QTR-A sensors on analog inputs 0-15
QTRSensorsAnalog qtr((unsigned char[]) {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}, NUM_SENSORS);
void setup() {
  
  esc.attach(ESC);
  esc.writeMicroseconds(STOP);//write stop first
  turn.attach( SERVO );
  turn.write( MID_ANGLE ); //start in the middle
  digitalWrite(LED, HIGH);
  for(int i = 0; i < 100; i++)
  {
    qtr.calibrate();
  }
  digitalWrite(LED, LOW);
  delay( 5000 );
  esc.writeMicroseconds( GO ); 
}

float P = 0;
float I = 0;
float D = 0;
int error = 0;
int prev_error = 0;
int correction = 0;
unsigned int sensors[NUM_SENSORS];

void loop() {
  int position = qtr.readLine(sensors,1,1);//returns val between 15000-0
  error = (position - MID_VAL)/100;  //error between 75 and -75. 75 left most sensor on line. -75 right most sensor on line
  P = kp * error;
  I += ki * error;
  D = kd * (error - prev_error);
  prev_error = error;
  correction = (P + I + D)/NORMALIZE;
  correction += MID_ANGLE;
  if(correction >= LEFT) turn.write(LEFT);
  else if(correction <= RIGHT) turn.write(RIGHT);
  else turn.write(correction);
  //perform a fast pulse for straight aways
  if(position <= 8700 && position >= 6200) { //if the car is pretty centered (centered is 7500) then go faster
    esc.writeMicroseconds( FAST );
    delay(7);
    esc.writeMicroseconds( STOP );
  }
  //perform a slow pulse for turns
  else{
    esc.writeMicroseconds( STOP );
    delay(45);
    esc.writeMicroseconds( GO) );
  }
}



