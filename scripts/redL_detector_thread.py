#!/usr/bin/env python3
#red light (redL) detector
import rospy
import threading

from std_msgs.msg import Int32
from std_msgs.msg import Bool

redL = Bool()

def kb_callback(k):
	global redL
	if(k.data == 114 or k.data == 82): # r: 114, R: 82
		redL.data = True;  # Red Light!!!
	else: # any other keys
		redL.data = False; # Non-red Light 

def publishing_thread():
  rate = rospy.Rate(5)
  while not rospy.is_shutdown():
    rl_pub.publish(redL)
    rate.sleep()

if __name__ == '__main__':
  rospy.init_node('redL_detector')
  kb_sub = rospy.Subscriber('/keyboard', Int32, kb_callback, queue_size=1)
  rl_pub = rospy.Publisher('/turtle1/redL', Bool, queue_size=1)
  worker = threading.Thread(target=publishing_thread)
  worker.start()
  rospy.spin()