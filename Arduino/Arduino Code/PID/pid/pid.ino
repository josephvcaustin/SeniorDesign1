#include <Servo.h>

const int Kp = 80;
const int Ki = 6;
const int Kd = 0;
const int NUM_SENSORS = 8; //number of sensors on each side
const int MAX_ERROR = Kp*( NUM_SENSORS-1 );
const int SENSOR_PIN_START = 0;
const int SENSOR_0 = 0;
const int SENSOR_PIN_END = 15;
const int SENSOR_PIN_MID = 7;
const int DELTA_THETA = 4; 
const int SERVO = 10;
const int ESC = 9;
const int MID_ANGLE = 103;
int THRESHOLD = 250;
const int FLAG = 7;
Servo turn;
Servo esc;
int OFF = 0; //gets incremented as sensors arrays come 
             //up empty (off the line), if it gets to 
             //a value of 2 that means we are completely off
int STOPPED = 0; //1 for a pending stop, 2 during a stop and 0 for moving
long STOP_TIME = 0; //time stamp for when we turn off the robot

void set_threshold( void ) {
  double sum = 0.0;
  
  for( int i = 0; i < 20; ++i ) {
     digitalWrite( FLAG, HIGH );
     delay( 100 );
     digitalWrite( FLAG, LOW );
     delay( 100 );
  }

  for( int i = SENSOR_0; i < NUM_SENSORS; ++i ) {
     sum += ( double )analogRead( i );
  }
  THRESHOLD = ( int ) ( sum/( double )NUM_SENSORS );

  delay( 1000 );

  for( int i = 0; i < 20; ++i ) {
     digitalWrite( FLAG, HIGH );
     delay( 100 );
     digitalWrite( FLAG, LOW );
     delay( 100 );
  }

  for( int i = SENSOR_0; i < NUM_SENSORS; ++i ) {
     sum += ( double )analogRead( i );
  }

  sum /= ( double )NUM_SENSORS;
  THRESHOLD += ( int ) sum;
  THRESHOLD /= 2;  

  delay( 1000 );

  for( int i = 0; i < 20; ++i ) {
     digitalWrite( FLAG, HIGH );
     delay( 100 );
     digitalWrite( FLAG, LOW );
     delay( 100 );
  }
}

void setup( ) {
  //setup pins to be used
  Serial.begin( 57600 );//test
  esc.attach( ESC );
  esc.writeMicroseconds( 1350 );
  turn.attach( SERVO );
  turn.write( MID_ANGLE ); //start in the middle
  //esc.writeMicroseconds( 1350 ); //start not moving 
  set_threshold( );
  delay( 5000 );
  esc.writeMicroseconds( 1430 );
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
/*int count_sets( int *buffer, int start, int end ) {
   for( int i = start; i <= end; ++i ) {
      if( buffer[i] >= 1 ) return i;
   }
   return 0;
}*/

//find highest set on left
int high_left( int *buffer, int len ) {
   for( int i = 7; i >= 0; --i ) {
	if( buffer[i] >= 1 ) {
                OFF = 0;
		return ( i+1 );
        }
   }
   OFF = 1;
   return 0;
}

//find highest set on right
int high_right( int *buffer, int len ) {
   for( int i = 0; i <= 7; ++i ) {
        if( buffer[i] >= 1 ) {
		OFF = 0;
        	return ( 8-i );
        }
   }
   OFF = 2;
   STOPPED = 1;
   return 0;
}

//calculates the error by the number
//of cells that we are off from the 
//desired state
int calculate_error( int *l_buffer, int *r_buffer, int len ) {
  int sets = 0;

  sets = high_left( l_buffer, len );
  //Serial.println( sets );
  if( sets > 1 ) return sets;

  sets = high_right( r_buffer, len );
  //Serial.println( sets );
  //Serial.println( "\n\n" );
  if(sets == 8) Serial.println("Sets = 8.");
  if( sets > 1 ) return -1*sets;
   
  if( OFF >= 2 ) return -8;
  
  else return 0;
}

//converts a voltage to a bit by
//using only a threshold for 1
int adc( int analog ) {
   if( ( double )analog >= THRESHOLD ) return 0;
   else return 1; 
}

//reads data into from the sensors
//into a left buffer and a right 
//buffer
void read_sensors( int *l_buffer, int *r_buffer, int len ) {
  
  //int zeros = 0;

  for( int i = SENSOR_PIN_START; i <= SENSOR_PIN_MID; ++i ) {
    l_buffer[i] = adc( analogRead( i+SENSOR_PIN_MID+1 ) );
    r_buffer[i] = adc( analogRead( i ) );
    //if( l_buffer[i] == 0 ) ++zeros;
    //if( r_buffer[i] == 0 ) ++zeros;
  }
  //if( zeros == 16 ) esc.writeMicroseconds( 1350 );
}

/***************** PID variables *****************/
int _err = 0; 
int _prev = 0; 
int _integral = 0; 
int _dt = 0;

//runs PID controlling only the turning of the car
void loop( ) {
  //register frist time stamp
  long t1 = millis(  );
  OFF = 0;

  int l_buffer[NUM_SENSORS]; //left sensors buffer
  int r_buffer[NUM_SENSORS]; //right sensor buffer

  //read sensor vals into buffer
  read_sensors( l_buffer, r_buffer, NUM_SENSORS ); 

  //calculate error based on new sensor values
  _err = calculate_error(  l_buffer, r_buffer, NUM_SENSORS  ); 

  //speed control
  if( STOPPED == 1 ) {
	esc.writeMicroseconds( 1350 );
	STOP_TIME = millis( );
        ++STOPPED;
  }
  if( STOPPED == 2 ) {
	_dt = millis( ) - STOP_TIME;
        if( _dt >= 500 ) {
		STOPPED = 0;
		esc.writeMicroseconds( 1430 );
        }
  }

  //get angle adjusment from decoder and save it to angle
  //int err = abs( _err ) > 2 ? _err-_prev : _err;
  //int coeff = _err < 0 ? -1*( ( ( _err*_err ) + 1 ) / 2 ) : ( ( ( _err*_err ) + 1 ) / 2 );
  int angle = MID_ANGLE + ( _err*DELTA_THETA );
  
  //do integral
  if( ( _err > 1 ) && ( _prev > 0 ) )
    angle += ( _prev * DELTA_THETA ) / 4;
  else _prev = 0;

  //accumulate error
  _prev = _err;

  //adjust car direction based on pid_out
  turn.write( angle );
}



