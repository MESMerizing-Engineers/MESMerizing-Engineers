#!/usr/bin/env python3

from std_msgs.msg import String
from geometry_msgs.msg import Twist, TwistStamped

import RPi.GPIO as GPIO
import serial

import rospy

class MotorController:
    def __init__(self):
        rospy.init_node("TwistToMotors")
        nodename = rospy.get_name()
        rospy.loginfo("%s started" % nodename)
        # defines the type of Twist messages being received
        self._stamped = rospy.get_param('~stamped', False)
        if self._stamped:
            self._cls = TwistStamped
            self._frame_id = rospy.get_param('~frame_id', 'base_link')
        else:
            self._cls = Twist
        # Being receiving Twist messages
        self.Twist_subscriber = rospy.Subscriber("cmd_vel", self._cls, self.callback_Twist)
        #self.PWM_publisher = rospy.Publisher('')
        # Setup Serial Communication to Arbotix platform
        try:
            serialPort = '/dev/ttyUSB0'
            self.ser = serial.Serial(serialPort,115200 , timeout = .5)
            self.ser.flush()
            rospy.loginfo("Started Serial Port %s" % serialPort)
        except:
            rospy.loginfo("Failed to detect serial port %s" % serialPort)
        # Setup Robot Parameters
        self.dl = 0
        self.dr = 0
        self.freq = 25  # hz default spark max freq = 50
        self.width = 20.5 #inches
        self.wheel_radius = 6 #inches
        self.maxRPM = 5500 #rpm
        self.maxSpeed = 1.0 # inches/sec
        self.pwm_ref = 0.0015 * self.freq * 256
        self.pwm_max_step = 0.0005 * self.freq * 256
        self.pwm_val_L = self.pwm_ref
        self.pwm_val_R = self.pwm_ref
        self.pan = 0.0
        self.tilt = 0.0
        # Configure PWM pins on Jetson
        output_pinL = 32
        output_pinR = 33
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(output_pinL, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(output_pinR, GPIO.OUT, initial=GPIO.LOW)
        self.motorL = GPIO.PWM(32, self.freq)
        self.motorR = GPIO.PWM(33, self.freq)
        # Start PWM with 0 RPM
        self.motorL.start(self.pwm_val_L)
        self.motorR.start(self.pwm_val_R)

    # Get Velocity from the Twist Node
    def callback_Twist(self, Twist_Msg):
        self.dl = round(Twist_Msg.linear.x ,3)    # forward velocity L
        self.dr = -1*round(Twist_Msg.angular.z,3)   # forward velocity R
        #self.pan = Twist_Msg.angular.x
        #self.tilt = Twist_Msg.angular.y

    def spin(self):
        r = rospy.Rate(self.freq)
        try:
            while not rospy.is_shutdown():
               	message = "0,0," + str(self.dl) + "," + str(self.dr) + "\n"
                self.ser.write(message.encode('ascii'))
                rospy.loginfo("Left Motor Speed: %f  Right Motor Speed: %f Time: %s",self.dl,self.dr, rospy.get_rostime() )
                r.sleep()
        finally:
            self.motorL.stop()
            self.motorR.stop()
            GPIO.cleanup()

if __name__ == '__main__':
    motorController = MotorController()
    motorController.spin()

        
