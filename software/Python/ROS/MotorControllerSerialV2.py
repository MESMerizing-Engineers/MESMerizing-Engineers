#!/usr/bin/env python3

from std_msgs.msg import String
from geometry_msgs.msg import Twist, TwistStamped
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
        self.dx = 0
        self.dr = 0
        self.pan = 0.0
        self.tilt = 0.0
        self.freq = 25  # hz default spark max freq = 50
        
        #Parameters currently unused
        self.width = 20.5 #inches
        self.wheel_radius = 3 #inches
        self.maxSpeed = 1.56 # m/sec
        

    # Get Velocity from the Twist Node
    def callback_Twist(self, Twist_Msg):
        self.dx = round(Twist_Msg.linear.x,3)    # forward velocity
        self.dr = round(Twist_Msg.angular.z,3)   # angular velocity
        self.pan = round(Twist_Msg.angular.x,3)  # pan speed
        self.tilt = round(Twist_Msg.angular.y,3) # tilt speed

    def spin(self):
        r = rospy.Rate(self.freq)
        try:
            while not rospy.is_shutdown():
                self.speedR = self.dx + self.dr
                self.speedL = self.dx - self.dr
                #message = str(self.pan) +","+ str(self.tilt) +","+ str(self.dx) + "," + str(self.dr*0.1) + "\n"
                message = "0.0,0.0," + str(self.dx) + "," + str(self.dr) + "\n"
                self.ser.write(message.encode('ascii'))
                rospy.loginfo("Left Motor Speed: %f  Right Motor Speed: %f Time: %s",self.speedL,self.speedR, rospy.get_rostime() )
                r.sleep()
        finally:


if __name__ == '__main__':
    motorController = MotorController()
    motorController.spin()

        
