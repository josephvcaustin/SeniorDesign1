//This program is used to control the
//car from user commands. This will allow
//us to transition from user commands to 
//the car reacting to sensor input

#include <Servo.h>

//Control constants
int SPEED_MAX = 2000;
int SPEED_MIN = 700;
int SPEED_STOP = 1350;
int FORWARD = 103;
int LEFT = 132;
int RIGHT = 75;


//Servo objects to control different motors
Servo motor;
Servo turn_servo;

//Control values for the motors
int car_speed = SPEED_STOP;
int turn = FORWARD;

void setup() {
  // put your setup code here, to run once:
  Serial.begin( 9600 );
  motor.attach( 9 );
  turn_servo.attach( 10 );
  motor.writeMicroseconds( SPEED_STOP );
  turn_servo.write( FORWARD );
}

void loop() {
  // put your main code here, to run repeatedly:
  char command = 'n';

  while( !Serial.available( ) );
  command = Serial.read( );

  switch( command ) {
    case 'w': 
      car_speed += 10; 
      break; 
      
    case 's': 
      car_speed -= 10; 
      break;
      
    case 'a': 
      turn += 5; 
      break; 
      
    case 'd': 
      turn -= 5; 
      break; 
      
    case 'o': 
      turn = FORWARD; 
      car_speed = SPEED_STOP; 
      break;
      
    case 'n': break;
    
    default: Serial.println( "Character not supported!\n" );
  }

  Serial.print( "speed: " ); Serial.print( car_speed ); Serial.print( " angle: " ); Serial.println( turn );

  motor.writeMicroseconds( car_speed );
  turn_servo.write( turn );
}
