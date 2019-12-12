#!/usr/bin/env python

import actionlib
import rospy

from math import sin, cos

from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

# Move base using navigation stack
class MoveBaseClient(object):

    def __init__(self):
        self.client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Waiting for move_base...")
        self.client.wait_for_server()

    def goto(self, x, y, theta, frame="map"):
        move_goal = MoveBaseGoal()
        move_goal.target_pose.pose.position.x = x


move_goal.target_pose.pose.position.y = y
        move_goal.target_pose.pose.orientation.z = sin(theta/2.0)
        move_goal.target_pose.pose.orientation.w = cos(theta/2.0)
        move_goal.target_pose.header.frame_id = frame
        move_goal.target_pose.header.stamp = rospy.Time.now()

        # TODO wait for things to work
        self.client.send_goal(move_goal)
        self.client.wait_for_result()

rospy.init_node("name")
# Localize robot
# creating a publisher to publish our initial pose automatically
# when the script starts (automatic localization)
# this will just always tell it it's starting at the same place
initial_x = -2.402 # CHANGE THIS VALUE TO CHANGE INITIAL POSITION
initial_y = 2.368 # CHANGE THIS VALUE TO CHANGE INITIAL POSITION
pub = rospy.Publisher("/initialpose", PoseWithCovarianceStamped, queue_size=10)
initial_pose = PoseWithCovarianceStamped()
initial_pose.header.frame_id = "/map"
initial_pose.header.stamp = rospy.Time.now()
initial_pose.pose.pose.position.x = initial_x
initial_pose.pose.pose.position.y = initial_y
# hardcoded these from doing:
# rostopic echo /initialpose
# while inputting 2D Pose Estimate in Rviz
initial_pose.pose.pose.orientation.z = -0.00925465500405 # CHANGE THIS VALUE TO CHANGE INITIAL POSITION
initial_pose.pose.pose.orientation.w = 0.999957174763 # CHANGE THIS VALUE TO CHANGE INITIAL POSITION

# You don't need to change this
initial_pose.pose.covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853892326654787]
# comment out the above part if you want to localize through rviz

# Move Robot
mb = MoveBaseClient()
pub.publish(initial_pose)
x1 = -1.8
y1 = 2.3
theta1 =1.5
x2 = -1.8
y2 = 4.3
theta2 =1.5
while True:
    mb.goto(x1, y1, theta1)
    rospy.sleep(5.0)
    mb.goto(x2,y2,theta2)
    rospy.sleep(5.0)
