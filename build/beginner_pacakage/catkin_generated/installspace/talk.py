#!/usr/bin/env python3

import rospy
from std_msgs.msg import String


def run_node():
    rospy.init_node('talker_py')
    talk_pub = rospy.Publisher('important_message', String, queue_size=100)
	
    rate = rospy.Rate(2)		
 	
    while not rospy.is_shutdown():
        import cv2 as cv
        import numpy as np

        videoCapture = cv.VideoCapture(0)

        prevCircle = None
        dist = lambda x1, y1, x2, y2: (x1 - x2) * 2 + (y1 - y2) * 2

        while True:
            ret, frame = videoCapture.read()
            if not ret:
                break

            grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            blurFrame = cv.GaussianBlur(grayFrame, (19, 19), 0)

            circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1.2, 100, param1=100, param2=30, minRadius=75, maxRadius=500)

            if circles is not None:
                circles = np.uint16(np.around(circles))
                chosen = None
                for i in circles[0, :]:
                    if chosen is None:
                        chosen = i
                    if prevCircle is not None:
                        if dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1]) <= dist(i[0], i[1], prevCircle[0], prevCircle[1]):
                            chosen = i
            
            
                    circle_radius = chosen[2]  
                    real_world_size = 0.1 
           
                    focal_length = 1000  
                    distance_to_camera = (real_world_size * focal_length) / (2 * circle_radius)
                    print("Coordinates (x, y):", chosen[0], chosen[1])
                    print("Distance to camera:", distance_to_camera, "meters")
                    msg1 = "Coordinates (x, y):"+ str(int(chosen[0])) + " " + str(int(chosen[1]))
                    msg2 = "Distance to camera:"+ str(distance_to_camera) + " meters"
                    talk_pub.publish(msg1)
                    rate.sleep()
                    talk_pub.publish(msg2)
                    rate.sleep()

                cv.circle(frame, (chosen[0], chosen[1]), 1, (0, 100, 100), 3)
                cv.circle(frame, (chosen[0], chosen[1]), chosen[2], (255, 0, 255), 3)
                prevCircle = chosen

            cv.imshow("circles", frame)

            key = cv.waitKey(1)
            if key == 27:
                break

        videoCapture.release()
        cv.destroyAllWindows()	
    
        
 		
if __name__ == '__main__':
    try:
        run_node()
    except rospy.ROSInterruptException:
        pass
