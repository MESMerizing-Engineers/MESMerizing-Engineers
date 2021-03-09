#define encoderLA 22
#define encoderLB 23
#define encoderRA 20 
#define encoderRB 21
#include <BioloidController.h>
#include <EncodersAB.h>


BioloidController bioloid = BioloidController(1000000);
double encResolution = 4096.0;
double speedL = 0.0; //Currently in terms of revolutions per second
double speedR = 0.0; //Change to velocity measurements later
unsigned long dt = 1; // Milli
unsigned long curTime = 0;
unsigned long prevTime = 0;
double scaler = 100000.0 // speed changes can be too small to print
                         // increase this to display 


void printSpeed(){
  Serial.print("  Right Speed: ");
  Serial.print(speedR);
  Serial.print("  Left Speed: ");
  Serial.println(speedL);
}

void setup(){
    Serial.begin(38400);
    Encoders.Begin();
}

void loop(){
  curTime = millis();
  dt = curTime - prevTime;
  speedR = ((double)Encoders.right/encResolution)/(dt/1000)*scaler;
  speedL = ((double)Encoders.left/encResolution)/(dt/1000)*scaler;
  Encoders.Reset();
  printSpeed();
  delay(50);
}
