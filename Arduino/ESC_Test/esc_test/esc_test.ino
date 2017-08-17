#include <Servo.h>

int MAX = 2000;
int MIN = 700;
int MID = 1350;

Servo esc;
Servo turn;

void setup() {
  // put your setup code here, to run once:
  Serial.begin( 9600 );
  esc.attach( 9 );
  turn.attach( 10 );

  /*esc.writeMicroseconds( MAX );
  while( !Serial.available( ) );
  Serial.read( );

  esc.writeMicroseconds( MIN );
  while( !Serial.available( ) );
  Serial.read( );

  esc.writeMicroseconds( MID );*/
}

void loop() {
  // put your main code here, to run repeatedly
  esc.writeMicroseconds( MID );
  while( !Serial.available( ) );
  Serial.read( );

  int i;
  for( i = MID; i <= 1500; i += 5 ) {
    esc.writeMicroseconds( i );
    delay( 250 );
  }

  int val = 103;
  for( i = i; i >= MID+50; i -= 10 ) {
    esc.writeMicroseconds( i );
    turn.write( --val );
    delay( 250 );
  }

  while( val > 75 ) {
    val -= 1;
    turn.write( val );
  }
  while( 1 );
}
