// Define Encoder Pins
#define encoderLA 22
#define encoderLB 23
#define encoderRA 20 
#define encoderRB 21
// Motor Pins
#define MOTORL 14
#define MOTORR 13
//#define F_CPU 1600000UL
//define pan and tilt servo IDs
#define PAN    1
#define TILT   2

// the F2 'C' bracket attached to the tilt servo creates a physical limitation to how far
// we can move the tilt servo. This software limit will ensure that we don't jam the bracket into the servo.
#define TILT_MAX 768 
#define TILT_MIN 256

//Upper/Lower limits for the pan servo - by defualt they are the normal 0-1023 (0-300) positions for the servo
#define PAN_MAX 1023 
#define PAN_MIN 0

//Default/Home position. These positions are used for both the startup position as well as the 
//position the servos will go to when they lose contact with the commander
#define DEFAULT_PAN 512
#define DEFAULT_TILT 512

//define analog pins that will be connected to the joystick pins
#define JOYPAN 0
#define JOYTILT 1

//generic deadband limits - not all joystics will center at 512, so these limits remove 'drift' from joysticks that are off-center.
#define DEADBANDLOW 480
#define DEADBANDHIGH 540

//Include necessary Libraries to drive the DYNAMIXEL servos  
#include <ax12.h>
#include <BioloidController.h>
#include <EncodersAB.h>
//

// Global Variable Declaration
BioloidController bioloid = BioloidController(1000000);
int pan;    //current position of the pan servo
int tilt;   //current position of the tilt servo  

int joyPanVal = 0;//current value of the pan joystick (analog 0) 0-1023
int joyTiltVal = 0;//current value of the tilt joystick (analog 1) 0-1023
int joyTiltMapped =0;//tilt joystick value, mapped  to -speed - speed
int joyPanMapped =0;//pan joystick value, mapped to -speed - speed

int speed = 10;//increase this to increase the speed of the movement

int countL = 0;
int countR = 0;
double speedForward = 0.0;
double speedRotate = 0.0; 
int speedL = 0; //Currently in terms of PWM width 
int speedR = 0; //Change to velocity measurements later
const byte numChars = 32;
char receivedChars[numChars] =" ";  
boolean newData = false;
int resolution;
double dutyL = 20000;
double dutyR = 20000;
int frequency = 50;
// Function Declartions

// Extract Values from formatted message
void parseMessage(){
  if(newData){
    char * strtokIndx;
    strtokIndx = strtok(receivedChars, ",");
    joyPanVal = atoi(strtokIndx)*1023;
    strtokIndx = strtok(NULL, ","); 
    joyTiltVal = atoi(strtokIndx)*1023;
    strtokIndx = strtok(NULL, ","); 
    speedForward = atoi(strtokIndx);
    strtokIndx = strtok(NULL, ","); 
    speedRotate = atoi(strtokIndx);
    newData = false;
  }
}
// Read Serial port for new messages
void readJetson() {
 static byte ndx = 0;
 char endMarker = '\n';
 char rc;
  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();
    if (rc != endMarker) {
      receivedChars[ndx] = rc;
      ndx++;
      if (ndx >= numChars) {
        ndx = numChars - 1;
      }
    }
    else {
      receivedChars[ndx] = '\0'; // terminate the string
      ndx = 0;
      newData = true;
    }
  }
}


// Define Custom PWM modes on pins 14 and 13
int pwm16Init(int freq){ // hz 
  DDRD |= (1 << 5)|(1<<4); // OC1A and OC1B pins are outputs
  resolution = (F_CPU/ (freq*64)) - 1; // Calculate and set the frequency
  Serial.println(resolution);
  // mode 14, clear OC1A on match and start timer
  TCCR1A = (1 << WGM11) | (1 << COM1A1) | (1 << COM1B1) ; //| (1<<COM1A0);
  TCCR1B = (1 << WGM13) | (1 << WGM12) | (1 << CS11); // prescale by 8
  TCCR1C = 0x00;
  //int dc = ;
  OCR1A = 3000; // 50% duty cycle
  ICR1 = 0x9C3F;
  //OCR1B = dc;
  
}

void pwm16Write(int dutyL, int dutyR){
    OCR1A = dutyL;
    OCR1B = dutyR;
}

void printEncoderCounts(){
  Serial.print("Left Count: ");
  Serial.print(Encoders.left);
  Serial.print("  Right Count: ");
  Serial.println(Encoders.right);
}
void poseMount(){
  //deadzone for pan jotystick - only change the pan value if the joystick value is outside the deadband
  if(joyPanVal > DEADBANDHIGH || joyPanVal < DEADBANDLOW){
     //joyPanVal will hold a value between 0 and 1023 that correspods to the location of the joystick. The map() function will convert this value
     //into a value between speed and -speed. This value can then be added to the current panValue to incrementley move ths servo 
     joyPanMapped = map(joyPanVal, -1023, 1023, -speed, speed);
     pan = pan + joyPanMapped;

     //enforce upper/lower limits for pan servo. This will ensure we do not move the servo to a position out of its physical bounds. 
     pan = max(pan, PAN_MIN);  //use the max() function to make sure the value never falls below PAN_MIN 
     pan = min(pan, PAN_MAX);  //use the min() function to make sute the value never goes above PAN_MAX 

   }
    
   //deadzone for tilt jotystick - only change the pan value if the joystick value is outside the deadband  
   if(joyTiltVal > DEADBANDHIGH || joyTiltVal < DEADBANDLOW){
     //joyTiltVal will hold a value between 0 and 1023 that correspods to the location of the joystick. The map() function will convert this value
     //into a value between speed and -speed. This value can then be added to the current panValue to incrementley move ths servo 
     joyTiltMapped = map(joyTiltVal, -1023, 1023, -speed, speed);
     tilt = tilt + joyTiltMapped;
          
     //enforce upper/lower limits for pan servo. This will ensure we do not move the servo to a position out of its physical bounds. 
     tilt = max(tilt, TILT_MIN);  //use the max() function to make sure the value never falls below TILT_MIN 
     tilt = min(tilt, TILT_MAX);  //use the min() function to make sute the value never goes above TILT_MAX 
     
   }
          
    //send pan and tilt goal positions to the pan/tilt servos 
    SetPosition(PAN,pan);
    SetPosition(TILT,tilt);
}
void setup(){
pinMode(0,OUTPUT);     // setup user LED
    digitalWrite(0, HIGH); // turn user LED on to show the program is running
    Serial.begin(38400);
    Encoders.Begin();
    //Set up Camera Mount
    pan = DEFAULT_PAN;//load default pan value for startup
    tilt = DEFAULT_TILT;//load default tilt value for startup
    bioloid.poseSize = 2;            //2 servos, so the pose size will be 2
    bioloid.readPose();              //find where the servos are currently
    bioloid.setNextPose(PAN,pan);    //prepare the PAN servo to the default position
    bioloid.setNextPose(TILT,tilt);  //preprare the tilt servo to the default position
    bioloid.interpolateSetup(2000);  //setup for interpolation from the current position to the positions set in setNextPose, over 2000ms
    while(bioloid.interpolating > 0) //until we have reached the positions set in setNextPose, execute the instructions in this loop
    {
      bioloid.interpolateStep();//move servos 1 'step
      delay(3);
    }
    pwm16Init(50); // Start PWM signal for Motors
}

void loop(){
  // Check for new serial data and update 
  readJetson();
  parseMessage();
  // Update the postion of the mount
  poseMount();
  speedR = speedForward + speedRotate;
  speedL = speedForward - speedRotate;
  dutyL = (0.0015 + .005*speedL/2) * frequency*(resolution);
  dutyR = (0.0015 + .005*speedR/2) * frequency*(resolution);
  // Read the Encoder values
  if(countL!= Encoders.left || countR != Encoders.right){
    //printEncoderCounts();
    countL = Encoders.left;
    countR = Encoders.right;
  }
  Serial.print(dutyL);
  Serial.println(resolution);
  //TO DO: SET Motor controllers
  //pwm16Write(dutyL,dutyR);
  // TODO Implement PID Control
  delay(20);
}
