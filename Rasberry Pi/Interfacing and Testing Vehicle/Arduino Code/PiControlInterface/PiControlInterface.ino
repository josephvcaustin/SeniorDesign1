#include <Servo.h>

int MAX_SPEED_FORWARD = 2000;
int MAX_SPEED_BACKWARD = 700;
int SPEED_STOP = 1350;

int STEER_STRAIGHT = 103;
int MAX_STEER_LEFT = 132;
int MAX_STEER_RIGHT = 75;

int CONSTANTS[6] = {MAX_SPEED_FORWARD, MAX_SPEED_BACKWARD, SPEED_STOP, STEER_STRAIGHT, MAX_STEER_LEFT, MAX_STEER_RIGHT};

//Serial Communication Command Constants

int QUERY = 10;
int ACKNOWLEDGE = 1001;
int SEND_STEERING = 11; //last 2 digits = value to set steering to
int SEND_THROTTLE = 12; //last 2 digits = value to set throttle to
int REQUEST_CONSTANT = 13; //Constant = max/min range, stored in consants array
int REQUEST_VALUE = 14; //value = active running value

int VALUE_MIDDLE = 50; //Throttle and steering inputs from Pi range from 1 to 99.

int current_speed = SPEED_STOP;
int current_turn = STEER_STRAIGHT;

Servo motor;
Servo turn_servo;

void setup(){
  Serial.begin(115200);
  motor.attach(9);
  turn_servo.attach(10);
  motor.writeMicroseconds(current_speed);
  turn_servo.writeMicroseconds(current_turn);
}

void loop()
{ 
  doCommand();
}

void doCommand()
{
  if (Serial.available() > 0)
  {
    int readIn = (Serial.read()-'0');
    
    if (readIn >= 1000) //Is a valid command
    {
      int command = readIn/1000; //First two digits indicate command
      int argument = readIn%1000; //Last two digits indicate argument
      
      if (readIn == QUERY) {Serial.println(ACKNOWLEDGE); return;}
      
      if (command == SEND_STEERING)
      {
        float argToValue = (MAX_STEER_LEFT - MAX_STEER_RIGHT)*(argument/((2*VALUE_MIDDLE)-1)) + MAX_STEER_RIGHT;  
        current_turn = (int)argToValue;
        Serial.println(current_turn); //Tell the Pi what value I'm turning
      }
      else if (command == SEND_THROTTLE)
      {
        float argToValue = (MAX_SPEED_FORWARD - MAX_SPEED_BACKWARD)*(argument/((2*VALUE_MIDDLE)-1)) + MAX_SPEED_FORWARD;  
        current_speed = (int)argToValue;
        Serial.println(current_speed); //Tell the Pi what my throttle is
      }
          
    }
    
  }
}

void Acknowledge()
{
  Serial.print(ACKNOWLEDGE + " "); Serial.print(current_turn + " "); Serial.print(current_speed + " "); 
}



