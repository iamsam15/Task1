#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def listenerCallback(msg):
    rospy.loginfo("Python talker said: " + msg.data)

if __name__ == '__main__':
    rospy.init_node('listener_py')
    
    rospy.Subscriber("important_message", String, listenerCallback)
    
    rospy.spin()
