#!/usr/bin/env python

import rospy
import actionlib
from control_msgs.msg import PointHeadAction, PointHeadGoal
from ar_track_alvar_msgs.msg import AlvarMarkers
from rail_manipulation_msgs.msg import SegmentedObjectList

global ph 
# Point the head using controller
class PointHeadClient(object):

    def __init__(self):
        self.client = actionlib.SimpleActionClient("head_controller/point_head", PointHeadAction)
        rospy.loginfo("Waiting for head_controller...")
        self.client.wait_for_server()

    def look_at(self, x, y, z, frame, duration=1.0):
        goal = PointHeadGoal()
        goal.target.header.stamp = rospy.Time.now()
        goal.target.header.frame_id = frame
        goal.target.point.x = x
        goal.target.point.y = y
        goal.target.point.z = z
        goal.min_duration = rospy.Duration(duration)
        self.client.send_goal(goal)
        self.client.wait_for_result()


def callback(msg):
    rospy.loginfo("Got a message!")
    for obj in msg.objects:
            ph.look_at(obj.center.x, obj.center.y, obj.center.z, msg.header.frame_id)
            rospy.sleep(1.0)

if __name__ == "__main__":
    # Create a node
    global ph
    rospy.init_node("tracker")
    ph = PointHeadClient()
    rospy.Subscriber("/rail_segmentation/segmented_objects", SegmentedObjectList, callback)
    rospy.spin()
