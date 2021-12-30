// Define Encoder Pins
#define encoderLA 22
#define encoderLB 23
#define encoderRA 20 
#define encoderRB 21
// Motor Pins
#define MOTORL 12
#define MOTORR 13
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
int joyTiltMapped = 0;//tilt joystick value, mapped  to -speedjoy- speed
int joyPanMapped = 0;//pan joystick value, mapped to -speedjoy to speedjoy 
int speedjoy= 10;//increase this to increase the speedjoyof the movement

// Variables for Motor Control
double speedForward = 0.0;
double speedRotate = 0.0; 
double setSpeedL = 0.0;
double setSpeedR = 0.0;
double prevSpeedL = 0.0; 
double prevSpeedR = 0.0; 
double accelLimit = 0.05; // MAX allowed change in motor speed  
unsigned int lowerBound = 2000;
unsigned int upperBound = 4000;
unsigned long resolution;
int frequency = 50;

// Used for Serial communication
const byte numChars = 46;
char receivedChars[numChars] =" ";  
boolean newData = false;

// Variables for Wheel Encoder 
double encResolution = 4096.0; // ticks in 1 revolution
double encSpeedL = 0.0; //Currently in terms of revolutions per second
double encSpeedR = 0.0; //Change to velocity measurements later
unsigned long dt = 1; // Milliseconds
unsigned long curTime = 0; 
unsigned long prevTime = 0;
double scaler = 100000.0; // speed changes can be too small to print
                         // increase this to display 

// Function Declartions

// Extract Values from formatted message
void parseMessage(){
  if(newData){
    char * strtokIndx;
    strtokIndx = strtok(receivedChars, ",");
    joyPanVal = atof(strtokIndx)*1023;
    strtokIndx = strtok(NULL, ","); 
    joyTiltVal = atof(strtokIndx)*1023;
    strtokIndx = strtok(NULL, ","); 
    speedForward = atof(strtokIndx);
    strtokIndx = strtok(NULL, ","); 
    speedRotate = atof(strtokIndx);
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
void pwm16Init(int freq){ // hz 
  //DDRD |= (1 << 5)|(1<<4); // OC1A and OC1B pins are outputs
  pinMode(MOTORL,OUTPUT); 
  pinMode(MOTORR,OUTPUT);
  resolution = 39999; // Calculate and set the frequency
  // mode 14, clear OC1A on match and start timer
  TCCR1A = (1 << WGM11) | (1 << COM1A1) | (1 << COM1B1) ; //| (1<<COM1A0);
  TCCR1B = (1 << WGM13) | (1 << WGM12) | (1 << CS11); // prescale by 8
  TCCR1C = 0x00;
  ICR1 = resolution;
  OCR1A = 3000; // Neutral Speed
  OCR1B = 3000;
}

void pwmWrite16(unsigned long dutyL, unsigned long dutyR){
  OCR1A = dutyR;
  OCR1B = dutyL; 
}
void setSpeed(double newSpeedL, double newSpeedR){
  if(newSpeedL - prevSpeedL >= accelLimit){ 
    newSpeedL = prevSpeedL + accelLimit;
  }else if(prevSpeedL - newSpeedL >= accelLimit){
    newSpeedL = prevSpeedL - accelLimit;
  }
  prevSpeedL = newSpeedL;
  newSpeedL *= 1000;
  newSpeedL = constrain(newSpeedL, -1000, 1000);

  if(newSpeedR - prevSpeedR >= accelLimit){ 
    newSpeedR = prevSpeedR + accelLimit;
  }else if(prevSpeedR - newSpeedR >= accelLimit){
    newSpeedR = prevSpeedR - accelLimit;
  }
  prevSpeedR = newSpeedR;
  newSpeedR *= 1000;
  newSpeedR = constrain(newSpeedR, -1000, 1000);

  unsigned long dutyCycleL = map(newSpeedL, -1000,1000, 2000, 4000);
  unsigned long dutyCycleR = map(newSpeedR, -1000,1000, 2000, 4000);
  pwmWrite16(dutyCycleL,dutyCycleR); 
  
  
}
void printSpeed(){
  Serial.print("  Right Speed: ");
  Serial.print(encSpeedR);
  Serial.print("  Left Speed: ");
  Serial.println(encSpeedL);
}
void poseMount(){
  //deadzone for pan jotystick - only change the pan value if the joystick value is outside the deadband
  if(joyPanVal > DEADBANDHIGH || joyPanVal < DEADBANDLOW){
     //joyPanVal will hold a value between 0 and 1023 that correspods to the location of the joystick. The map() function will convert this value
     //into a value between speedjoyand -speed. This value can then be added to the current panValue to incrementley move ths servo 
     joyPanMapped = map(joyPanVal, -1023, 1023, -speedjoy, speedjoy);
     pan = pan + joyPanMapped;

     //enforce upper/lower limits for pan servo. This will ensure we do not move the servo to a position out of its physical bounds. 
     pan = max(pan, PAN_MIN);  //use the max() function to make sure the value never falls below PAN_MIN 
     pan = min(pan, PAN_MAX);  //use the min() function to make sute the value never goes above PAN_MAX 

   }
    
   //deadzone for tilt jotystick - only change the pan value if the joystick value is outside the deadband  
   if(joyTiltVal > DEADBANDHIGH || joyTiltVal < DEADBANDLOW){
     //joyTiltVal will hold a value between 0 and 1023 that correspods to the location of the joystick. The map() function will convert this value
     //into a value between speedjoyand -speed. This value can then be added to the current panValue to incrementley move ths servo 
     joyTiltMapped = map(joyTiltVal, -1023, 1023, -speedjoy, speedjoy);
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
    Serial.begin(115200);
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
  setSpeedR = speedForward - speedRotate;
  setSpeedL = -1.0*(speedForward + speedRotate);
  setSpeed(setSpeedL,setSpeedR);
  // TODO Implement PID Control
  delay(50);
}
