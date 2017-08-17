#include <Servo.h>

const int Kp = 80;
const int Ki = 6;
const int Kd = 0;
const int NUM_SENSORS = 1; //number of sensors on each side
const int MAX_ERROR = Kp;//*( NUM_SENSORS-1 );
const int SENSOR_PIN_START = 0;
const int SENSOR_PIN_END = 15;
const int SENSOR_PIN_MID = 7;
const int DELTA_THETA = 1; //CHANGED
const int SERVO = 10;
const int ESC = 9;
const int MID_ANGLE = 103;
const double V_T = 1.8; //threshold voltage for Vih
Servo turn;
Servo esc;

//******** TEMP *********//
const int LEFT = 51;
const int RIGHT = 53;


void setup( ) {
  //setup pins to be used
  //Serial.begin( 9600 );//test
  esc.attach( ESC );
  turn.attach( SERVO );
  turn.write( MID_ANGLE ); //start in the middle
  esc.write( 1350 ); //start not moving
  delay( 2000 );
  esc.writeMicroseconds( 1390 );
}

//runs the PID calculations and returns the 
//correction value to be read by the decoder
int pid( int err, int &prev_err, int &integral, int Kp, int Ki, int Kd, int dt ) {
  int p = Kp * err;
  p = (int)( ( (double)p/MAX_ERROR )*(double)NUM_SENSORS ); //normalize max error to NUM_SENSORS
  
  if( dt == 0 ) return p; //to avoid division by 0 on the first call
			  //we only use p on the first run
  
  integral += err*dt;
  int i = Ki*integral;
  i = (int)( ( (double)i/MAX_ERROR )*(double)NUM_SENSORS );
  
  int deriv = ( err-prev_err ) / dt;
  int d = Kd*deriv;
  d = (int)( ( (double)d/MAX_ERROR )*(double)NUM_SENSORS );
	
  int output = p + i + d;
  if( abs( output ) > NUM_SENSORS ) output = output < -1*NUM_SENSORS ? -1*NUM_SENSORS : NUM_SENSORS;

  prev_err = err;

  return output;
}

//takes the pid output and decodes it
//then output a turning angle
int pid_decoder( int pid_out, int delta_theta ) {
    //delta theta is the incremental angle
    //which can be used to turn the car
    //This can be the angle between sensors 
    //measured from the center of the front 
    //of the car or it can be another value
    //set by the user
    return MID_ANGLE + ( pid_out*delta_theta ); 
}

//counts how many elements are set in a buffer
//set being > 0
int count_sets( int *buffer, int len ) {
   int count = 0;
   for( int i = 0; i < len; ++i ) {
      if( buffer[i] >= 1 ) ++count;
   }
   return count;
}

//calculates the error by the number
//of cells that we are off from the 
//desired state
int calculate_error( int *l_buffer, int *r_buffer, int len ) {
  /*if( left == 1 && right == 0 ) return -1;
  else if( left == 0 && right == 1 ) return 1;
  else if( left == 1 && right == 1 ) return -3;
  else return 0;*/
  int sets = 0;
  if( ( sets = count_sets( l_buffer, len ) ) > 1 ) return -1*sets + 1;
  else if( ( sets = count_sets( r_buffer, len ) ) > 1 ) return sets-1;
}

//converts a voltage to a bit by
//using only a threshold for 1
int adc( int analog, double Vih ) {
   if( ( double )analog > Vih ) return 1;
   else return 0; 
}

//reads data into from the sensors
//into a left buffer and a right 
//buffer
void read_sensors( int *l_buffer, int *r_buffer, int len ) {
  
  for( int i = SENSOR_PIN_START; i <= SENSOR_PIN_MID; ++i ) {
    l_buffer[i] = adc( analogRead( i ), V_T );
    r_buffer[i] = adc( analogRead( i+SENSOR_PIN_MID+1 ), V_T );
  }
}

/***************** PID variables *****************/
int _err = 0; 
int _prev_err = 0; 
int _integral = 0; 
int _dt = 0;

//runs PID controlling only the turning of the car
void loop( ) {
  //register frist time stamp
  long t1 = millis(  );

  int l_buffer[NUM_SENSORS]; //left sensors buffer
  int r_buffer[NUM_SENSORS]; //right sensor buffer

  //read sensor vals into buffer
  read_sensors( l_buffer, r_buffer, NUM_SENSORS ); 

  //calculate error based on new sensor values
  _err = calculate_error(  l_buffer, r_buffer, NUM_SENSORS  ); 

  //get angle adjusment frmo decoder and save it to angle
  int angle = MID_ANGLE + ( _err*DELTA_THETA );
  
  //do integral
  if( ( _err > 0 ) && ( _integral > 0 ) )
    angle += _integral * DELTA_THETA;
  else _integral = 0;

  //accumulate error
  _integral += _err;

  //get pid adjustment and save it into pid_out
  //int pid_out = pid( _err, _prev_err, _integral, Kp, Ki, Kd, _dt ); 

  //adjust car direction based on pid_out
  turn.write( angle );

  //register second time stamp
  long t2 = millis(  );
  
  //get delta t for next loop iteration
  _dt = t2-t1;
}



