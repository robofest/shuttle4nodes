#!/usr/bin/env python3
#
# TT control
#

import rospy
from std_msgs.msg import Bool
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen

red_light = False;
lsz_state = False; # lsz: low speed zone
vel_msg = Twist()
turtle1_pen = rospy.ServiceProxy('turtle1/set_pen', SetPen) # Service call name, service class

def stopTurtle():
	vel_msg.linear.x = 0
	vel_msg.angular.z = 0
	velocity_pub.publish(vel_msg)

def redL_cb(r):
	global red_light
	if(r.data == True): # stop
		red_light = True;
	else:
		red_light = False;

def lsz_cb(lsz):
	global lsz_state
	if(lsz.data == True):
		lsz_state = True	
	else:
		lsz_state = False;
		

# publish Twist message v based on the current red light and speed zone states.
# Use 0.5 as the speed for the low speed zone
def shuttle2points_cb(v):
	vel_msg.linear.x = v.linear.x 
	if(red_light == True): # red light seen
		stopTurtle()
	else:                  # no red light
		if(lsz_state == True): # low speed zone
			if (vel_msg.linear.x > 0.0):
				vel_msg.linear.x = 0.2
			else:
				vel_msg.linear.x = -0.2
			srv_resp = turtle1_pen(255,0,0,5,0)
			velocity_pub.publish(vel_msg);
		else: # normal zone
			srv_resp = turtle1_pen(0,0,0,5,0)
			velocity_pub.publish(v)

if __name__ == '__main__':
  rospy.init_node('tt_control')
  velocity_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1)
  
  shuttle_sub = rospy.Subscriber("/turtle1/cmd_vel0", Twist, shuttle2points_cb, queue_size=1);
  redL_sub = rospy.Subscriber("/turtle1/redL", Bool, redL_cb, queue_size=1);
  lsz_sub = rospy.Subscriber("/turtle1/lsz", Bool, lsz_cb, queue_size=1); # low speed zone detector
  rospy.spin() # to hold this node
