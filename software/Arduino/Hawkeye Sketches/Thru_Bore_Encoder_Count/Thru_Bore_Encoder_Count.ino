#define encoderLA 6
#define encoderLB 7
#define encoderRA 20 
#define encoderRB 21
#define MOTORL 14
#define MOTORR 15
#include <BioloidController.h>
#include <EncodersAB.h>


BioloidController bioloid = BioloidController(1000000);
int countL = 0;
int countR = 0;
int speedL = 0; //Currently in terms of PWM width 
int speedR = 0; //Change to velocity measurements later
const byte numChars = 32;
char receivedChars[numChars] =" ";  
boolean newData = false;

void parseMessage(){
  if(newData){
    char * strtokIndx;
    strtokIndx = strtok(receivedChars, ",");
    speedL = atoi(strtokIndx);
    strtokIndx = strtok(NULL, ","); 
    speedR = atoi(strokIndx);
    newData = false;
  }
}

void recvWithEndMarker() {
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



void setup(){
    Serial.begin(38400);
    Encoders.Begin();
    pinMode(MOTORL, OUTPUT)
    pinMode(MOTORR, OUTPUT)
}

void loop(){
  recvWithEndMarker();
  parseMessage();
  if(countL!= Encoders.left || countR != Encoders.right){
    Serial.print("Left Count: ");
    Serial.print(Encoders.left);
    Serial.print("  Right Count: ");
    Serial.println(Encoders.right);
    countL = Encoders.left;
    countR = Encoders.right;
  }
  delay(1);
}
