#!/usr/bin/env python3
#
# Shuttle 2 points forever 
# CJ F2021
#

import rospy
from std_msgs.msg import Bool
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

trtl_pose = Pose()

def pose_cb(pose_msg): # get current x, y, orientation
	global trtl_pose
	trtl_pose.x     = pose_msg.x
	trtl_pose.y     = pose_msg.y
	trtl_pose.theta = pose_msg.theta # current absolute orientation of the turtle

def move(vel, goal_x):
	vel_msg = Twist()
	vel_msg.linear.x = vel

	rate = rospy.Rate(10) # 100 ms
	if(vel > 0):
		velocity_pub.publish(vel_msg)
		while( trtl_pose.x < goal_x ):
			velocity_pub.publish(vel_msg)
			rate.sleep()
	else: # negative velocity
		velocity_pub.publish(vel_msg)
		while( trtl_pose.x > goal_x ):
			velocity_pub.publish(vel_msg);
			rate.sleep()

def init_trtl():
  # the turtle needs sometime to publish pose data in the beginning
  while trtl_pose.x == 0.0:  #the initial x position data must be 5.54444
    pass

if __name__ == '__main__':
  rospy.init_node('shuttle_2points')
  velocity_pub = rospy.Publisher('/turtle1/cmd_vel0', Twist, queue_size=1)
  pose_sub = rospy.Subscriber('/turtle1/pose', Pose, pose_cb, queue_size=1)
  init_trtl()

  move(3, 10) # go to (10, current y) location
  while not rospy.is_shutdown():
    move(-3, 1)
    move(+3, 10)
  # ros::spin() # not necessary due to the endless while above 
