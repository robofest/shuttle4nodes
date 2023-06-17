#!/usr/bin/env python3

import time
import rospy

#
# to find Service classes?      $ rossrv list
# to find Service names?        $ rosservice list
#
from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import Spawn
from turtlesim.srv import SetPen
from std_srvs.srv  import Empty as EmptyServiceCall # for clear back grnd


rospy.init_node("teleporting_node")

clear_background = rospy.ServiceProxy('clear', EmptyServiceCall)

spawn_turtle = rospy.ServiceProxy('spawn', Spawn)

spawn_turtle(5,5,45, "turtle2")  #x,y,theta
time.sleep(3)
print('wait for 3 seconds...')
                                     # Service call name           imported Service class 
turtle1_teleport = rospy.ServiceProxy('turtle1/teleport_absolute', TeleportAbsolute)
turtle2_teleport = rospy.ServiceProxy('turtle2/teleport_absolute', TeleportAbsolute)
turtle1_pen = rospy.ServiceProxy('turtle1/set_pen', SetPen)

turtle1_pen(255, 0, 0, 10, 0)
turtle1_teleport(10,2,0)

turtle2_teleport(2,2,0)
print('teleportation completed')
