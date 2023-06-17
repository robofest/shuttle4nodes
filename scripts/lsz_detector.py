#!/usr/bin/env python3
#
# LSZ (Low Speed Zone) Detector
#

import rospy
from std_msgs.msg import Int32
from std_msgs.msg import Bool
from turtlesim.msg import Pose

tt_pose = Pose()
lsz = Bool()

def init_turtle():
  # the turtle needs sometime to publish pose data in the beginning
  while tt_pose.x == 0.0:  #the initial x position data must be 5.54444
    pass

def pose_cb(p): # get current x, y, orientation
	global tt_pose, lsz
	tt_pose.x = p.x

	if (p.x > lsz_begin and p.x < lsz_end): # LSZ
		if(lsz.data == False):
			print(f"LSZ entered at {tt_pose.x}")
		lsz.data = True;
	else:
		if(lsz.data == True):
			print(f"Normal Speed Zone entered at {tt_pose.x}")
		lsz.data = False;
	lsz_pub.publish(lsz)

if __name__ == '__main__':
  rospy.init_node('lsz_detector')
  lsz_begin = rospy.get_param('lsz_begin')
  lsz_end = rospy.get_param('lsz_end')
  pose_sub = rospy.Subscriber('/turtle1/pose', Pose, pose_cb, queue_size=1)
  lsz_pub = rospy.Publisher('/turtle1/lsz', Bool, queue_size=1)
  lsz.data = False # in the beginning at 5.54, it must be false

  init_turtle()
  rospy.spin() # to hold this node
