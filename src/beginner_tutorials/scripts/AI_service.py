#!/usr/bin/env python

from __future__ import print_function
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from beginner_tutorials.srv import AI, AIResponse
import rospy

bridge = CvBridge()

def predictNumberFromImage(imgMsg):

    img = bridge.imgmsg_to_cv2(imgMsg)

    predection = 7 #hardcoded example

    #load model here and do prediction

    return predection


def prediction_server():

        rospy.init_node('prediction_server')
        s = rospy.Service('number_prediction_service', AI, predictNumberFromImage)

        print("ready to make a prediction")

        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()

if __name__ == "__main__":
    prediction_server()