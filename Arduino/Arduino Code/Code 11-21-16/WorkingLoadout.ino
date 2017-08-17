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
#define GO 1420
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
  //esc.writeMicroseconds( 1350 ); //start not moving
  digitalWrite(LED, HIGH);
  for(int i = 0; i < 100; i++)
  {
    qtr.calibrate();
  }
  digitalWrite(LED, LOW);
  delay( 5000 );
  esc.writeMicroseconds( GO ); 
  delay(100);
  esc.writeMicroseconds( SLOW );
}

float P = 0;
float I = 0;
float D = 0;
int error = 0;
int prev_error = 0;
int correction = 0;
unsigned int sensors[NUM_SENSORS];

void loop() {
  // put your main code here, to run repeatedly:
  int position = qtr.readLine(sensors,1,1);
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
  esc.writeMicroseconds( STOP );
  delay(35);
  esc.writeMicroseconds( GO );
}



