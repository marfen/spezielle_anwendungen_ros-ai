#!/usr/bin/env python


import rospy
from sensor_msgs.msg import Image
from beginner_tutorials.msg import IntWithHeader
from cv_bridge import CvBridge
import cv2
import rospkg
import random

imagepick = random.randint(0, 9)

def talker():
    # initialize cvbridge
    bridge = CvBridge()

    # publisher image topic
    imagePub = rospy.Publisher('image', Image, queue_size=1)

    #publisher integer topic
    intPub = rospy.Publisher('integer', IntWithHeader, queue_size=1)

    imagepick = random.randint(0,9)
    # load image
    rospack = rospkg.RosPack()
    image_path = rospack.get_path('beginner_tutorials') + '/mnist/'

    if imagepick == 0:
        img = cv2.imread(image_path + 'mnist_0.png')
    elif imagepick == 1:
        img = cv2.imread(image_path + 'mnist_1.png')
    elif imagepick == 2:
        img = cv2.imread(image_path + 'mnist_2.png')
    elif imagepick == 3:
        img = cv2.imread(image_path + 'mnist_3.png')
    elif imagepick == 4:
        img = cv2.imread(image_path + 'mnist_4.png')
    elif imagepick == 5:
        img = cv2.imread(image_path + 'mnist_5.png')
    elif imagepick == 6:
        img = cv2.imread(image_path + 'mnist_6.png')
    elif imagepick == 7:
        img = cv2.imread(image_path + 'mnist_7.png')
    elif imagepick == 8:
        img = cv2.imread(image_path + 'mnist_8.png')
    elif imagepick == 9:
        img = cv2.imread(image_path + 'mnist_9.png')


    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1) # 10hz

    while not rospy.is_shutdown():

        #create imagemsg from image
        imageMsg = Image()
        imageMsg = bridge.cv2_to_imgmsg(img, encoding="bgr8")

        #create int message
        intMsg = IntWithHeader()
        intMsg.data = imagepick

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
