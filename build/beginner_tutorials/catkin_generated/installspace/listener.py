#!/usr/bin/env python3

## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

#initialize bridge
bridge = CvBridge()

def callback(ImageMsg):
    # rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

    # transform image msg to cv2
    img = bridge.imgmsg_to_cv2(ImageMsg)


    # make image grayscaled
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # make it B/W
    (thresh, img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)  # Image is turned into an black and white image

    # publish image to topic processed image
    imgPubNext = rospy.Publisher('processedImage', Image, queue_size=1)

    # create imagemsg from image again
    imgMsg = bridge.cv2_to_imgmsg(img)

    rate = rospy.Rate(1)

    while not rospy.is_shutdown():

        # publish image Message
        imgPubNext.publish(imgMsg)
        rate.sleep()

    #display image
    cv2.imshow('img', img)
    cv2.waitKey(0)



    #publish image to new topic
    # afterCropPub = rospy.Publisher('afterCrop', Image, queue_size=10)
    # afterCropPub.publish(crop_img)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('image', Image, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
