#!/usr/bin/env python


import rospy
from sensor_msgs.msg import Image
from beginner_tutorials.msg import IntWithHeader
from cv_bridge import CvBridge
import cv2
import rospkg


def talker():
    # initialize cvbridge
    bridge = CvBridge()

    # publisher image topic
    imagePub = rospy.Publisher('image', Image, queue_size=1)

    #publisher integer topic
    intPub = rospy.Publisher('integer', IntWithHeader, queue_size=1)

    # load image
    rospack = rospkg.RosPack()
    image_path = rospack.get_path('beginner_tutorials') + '/mnist/'
    img = cv2.imread(image_path + 'mnist_0.png')


    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1) # 10hz

    while not rospy.is_shutdown():

        #create imagemsg from image
        imageMsg = Image()
        imageMsg = bridge.cv2_to_imgmsg(img, encoding="bgr8")

        #create int message
        intMsg = IntWithHeader()
        intMsg.data = 7

        #rospy.loginfo(intMsg)

        # publish both
        imagePub.publish(imageMsg)
        intPub.publish(intMsg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
