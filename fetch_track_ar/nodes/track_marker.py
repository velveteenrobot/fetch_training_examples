#!/usr/bin/env python

import rospy
import actionlib
from control_msgs.msg import PointHeadAction, PointHeadGoal
from ar_track_alvar_msgs.msg import AlvarMarkers

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
    rospy.logdebug_throttle(2, "Got a marker message")
    if not msg.markers:
        rospy.logwarn_throttle(2, "No markers detected.")
    for marker in msg.markers:
        if marker.id == 8:
            ph.look_at(marker.pose.pose.position.x, marker.pose.pose.position.y, marker.pose.pose.position.z, marker.header.frame_id)
            rospy.loginfo("Saw correct marker")
        elif marker.id == 1:
            rospy.logerr("Node name: Saw thing labeled 1")
        else:
            rospy.logdebug("Wrong marker number: " + str(marker.id))
if __name__ == "__main__":
    # Create a node
    global ph
    rospy.init_node("tracker")
    ph = PointHeadClient()
    rospy.Subscriber("/ar_pose_marker_throttle", AlvarMarkers, callback)
    rospy.spin()
