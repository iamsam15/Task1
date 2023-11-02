!/usr/bin/env python

import rospy
from std_msgs.msg import String 
def run_node():
	rospy.init_node('talker_python')
	talk_pub = rospy.Publisher('important_message', String, queue_size=100)
	rate = rospy.Rate(2) # hz
	
	count = 0
	while not rospy.is_shutdown():
		if count%2 == 0:
			msg = "count is :" + str(int(count/2))
		else:
			msg = "count is :" +str(int(count/2)) + " and a half"
		count += 1
		
		talk_pub.publish(msg)
		rate.sleep()
		

if __name__=='__main__':
	try :
		run_node()
	except rospy.ROSInterruptException:
		pass
