#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan

pub = rospy.Publisher('base_scan_copy', LaserScan, queue_size=10)

def callback(scan):
    rospy.loginfo(rospy.get_caller_id() + "The frame_id is %s", scan.header.frame_id)
    pub.publish(scan)

if __name__ == '__main__':
    rospy.init_node('repub_node', anonymous=True)
    rospy.Subscriber("base_scan", LaserScan, callback)
    rospy.spin()
