#include <Servo.h>

int MAX_SPEED_FORWARD = 2000;
int MAX_SPEED_BACKWARD = 700;
int SPEED_STOP = 1350;

int STEER_STRAIGHT = 103;
int MAX_STEER_LEFT = 132;
int MAX_STEER_RIGHT = 75;

int COMMAND_SPEEDUP = 3;
int COMMAND_MAINTAIN = 2;
int COMMAND_SLOWDOWN = 1;
int COMMAND_STOP = 0;

int COMMAND_GORIGHT = 3;
int COMMAND_GOSTRAIGHT = 2;
int COMMAND_GOLEFT = 1;

int HANDSHAKE = 123;
int ACKNOWLEDGE = 456;
int VALIDCOMMANDRANGE = 34;

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
  establishComms();
  
  getCommand();
}

void establishComms()
{
  while(true)
  {
    if (Serial.available() > 0)
    {
      if ((Serial.read()-'0') == HANDSHAKE) {Serial.println(ACKNOWLEDGE); return;}
    }
    delay(10);
  } 
}

void getCommand()
{
  if (Serial.available() > 0)
  {
      int readIn = (Serial.read()-'0');
      if (readIn == HANDSHAKE) {Serial.println(ACKNOWLEDGE); return;}
      else if(readIn < VALIDCOMMANDRANGE)
      {
         //Read in a two digit integer from the Pi.
         //Tens place: 1 = turn left, 2 = go straight, 3 = turn right.
         //Ones place: 0 = brake, 1 = slow down, 2 = maintain speed, 3 = go faster.
         int steering = readIn/10;
         int driving = readIn%10;
        
         if (steering == COMMAND_GOLEFT) 
         {
           if(current_turn < MAX_STEER_LEFT) current_turn++;
         }
         else if (steering == COMMAND_GORIGHT)
         {
           if(current_turn > MAX_STEER_RIGHT) current_turn--;
         }
         else if (steering == COMMAND_GOSTRAIGHT) {/*go straight*/}
         else 
         {/*slam on the brakes*/
           current_speed = SPEED_STOP;
         }
         
         if (driving == COMMAND_SLOWDOWN) 
         {/*slow down*/
           if(current_speed > MAX_SPEED_BACKWARD) current_speed--;
         }
         else if (driving == COMMAND_SPEEDUP) 
         {/*speed up*/
           if(current_speed < MAX_SPEED_FORWARD) current_speed++;
         }
         else if (driving == COMMAND_MAINTAIN) {/*maintain speed*/}
         else 
         {/*slam on the brakes*/
           current_speed = SPEED_STOP;
         }
         
      }
      else 
      {/*slam on the brakes*/
        current_speed = SPEED_STOP;
      }
  }
}

void Acknowledge()
{
  Serial.print(ACKNOWLEDGE + " "); Serial.print(current_turn + " "); Serial.print(current_speed + " "); 
}



