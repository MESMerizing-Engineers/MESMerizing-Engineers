#define MOTORL 9//Must be pin 9 or 10 on the uno
#define MOTORR 10//Must be pin 9 or 10 on the uno

double prevSpeed = 0.0; 
double accelLimit = 0.01; // MAX allowed change in motor speed  
unsigned int lowerBound = 2000;
unsigned int upperBound = 4000;
unsigned long resolution;

void pwmInit16(int freq){ // hz 
  resolution = (F_CPU/ (freq*8)) - 1; // Calculate and set the frequency
  // mode 14, clear OC1A on match and start timer
  TCCR1A = (1 << WGM11) | (1 << COM1A1) | (1 << COM1B1) ; //| (1<<COM1A0);
  TCCR1B = (1 << WGM13) | (1 << WGM12) | (1 << CS11); // prescale by 8
  TCCR1C = 0x00;
  ICR1 = resolution;
  OCR1A = resolution/2; // 50% duty cycle
  OCR1B = resolution/2;
}

void pwmWrite16(unsigned int pin, unsigned long duty){
  switch(pin){
    case MOTORL: OCR1A = duty; break;
    case MOTORR: OCR1B = duty; break;
  }
}

// Change the speed of a motor
// newspeed is a value from -1 to 1 
void setSpeed(unsigned int pin, double newSpeed){
  if(newSpeed - prevSpeed >= accelLimit){ 
    newSpeed = prevSpeed + accelLimit;
  }else if(prevSpeed - newSpeed >= accelLimit){
    newSpeed = prevSpeed - accelLimit;
  }
  newSpeed *=1000;
  newSpeed = constrain(newSpeed, -1000, -1000);
  unsigned long dutyCycle = map(newSpeed, -1000,1000, 2000, 4000);
  pwmWrite16(pin, dutyCycle); 
  prevSpeed = newSpeed;
}
  
void setup(){
 pinMode(MOTORL,OUTPUT); 
 pinMode(MOTORR,OUTPUT);
 pwmInit16(50);
}

void loop(){
 //put main code here :) 
}

