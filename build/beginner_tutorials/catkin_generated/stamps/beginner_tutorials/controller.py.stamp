#!/usr/bin/env python

from __future__ import print_function
from cv_bridge import CvBridge

import sys
import rospy
import numpy as np
import message_filters

from sensor_msgs.msg import Image
from beginner_tutorials.msg import IntWithHeader
from beginner_tutorials.srv import *

bridge = CvBridge()


def prediction_service_client(imageMsg):
    rospy.wait_for_service('number_prediction_service')
    try:
        number_prediction_service = rospy.ServiceProxy('number_prediction_service', AI)
        response = number_prediction_service(imageMsg)
        return response.result
    except rospy.ServiceException as e:
        print("Sevice call failes: %s" % e)


def callback(img_msg, int_with_header):
    # image to cv2
    img = bridge.imgmsg_to_cv2(img_msg)
    trueInt = int_with_header.data

    #save pairs in dict
    imgIntPair = {
        "image": img,
        "trueInt": trueInt
    }

    imageMsg = bridge.cv2_to_imgmsg(img)
    prediction = prediction_service_client(imageMsg)

    #if imgIntPair.trueInt == prediction:
    #    print("prediction right")
    #else:
    #    print("prediction wrong")

    # prints size of the image
    rospy.loginfo(np.shape(imageMsg))

    # rospy.loginfo(intMsg)
    # rospy.loginfo(int_with_header.data)


def listener():
    rospy.init_node("controller", anonymous=True)
    imageSub = message_filters.Subscriber("processedImage", Image)
    intSub = message_filters.Subscriber("integer", IntWithHeader)
    ts = message_filters.TimeSynchronizer([imageSub, intSub], 10)
    ts.registerCallback(callback)
    rospy.spin()

if __name__ == "__main__":
    listener()