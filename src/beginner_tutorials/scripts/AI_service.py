#!/usr/bin/env python

from __future__ import print_function
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import torch as t

from beginner_tutorials.srv import AI, AIResponse
import rospy
import rospkg
#from beginner_tutorials.pytorch_models.Model1 import Model1
#from pytorch_models.Model2 import Model2


bridge = CvBridge()

def predictNumberFromImage(imgMsg):

    rospack = rospkg.RosPack()

    img = bridge.imgmsg_to_cv2(imgMsg.image)

    #alles Auskommentiert wegen Problemen beim Importieren der Models


    # zum wechseln eine der beiden auskommentieren
    #model1_path = rospack.get_path('beginner_tutorials') + '/pytorch_models/Model1'
    #model = Model1()
    #model.load_state_dict(t.load(model1_path))

    #model2_path = rospack.get_path('beginner_tutorials') + '/pytorch_models/Model2'
    #model = Model2()
    #model.load_state_dict(t.load(model2_path))

    #model.eval()

    #prediction = model.predict()


    #return prediction


def prediction_server():

        rospy.init_node('prediction_server')
        s = rospy.Service('number_prediction_service', AI, predictNumberFromImage)

        print("ready to make a prediction")

        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()

if __name__ == "__main__":
    prediction_server()