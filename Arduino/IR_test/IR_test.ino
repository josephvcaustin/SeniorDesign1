//Code to test the IR sensors
//for functionality

void setup() {
  Serial.begin( 9600 );
}

void loop() {
  //prints out the value in analog pin 0
  int val = analogRead( 0 );
  delay( 25 );
  Serial.println( val );
}














