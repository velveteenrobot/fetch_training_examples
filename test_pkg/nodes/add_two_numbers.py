#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from test_pkg.msg import operands
from std_msgs.msg import Float32

pub = rospy.Publisher('sum', Float32, queue_size=10)

def callback(operands):
    rospy.loginfo(rospy.get_caller_id() + "The numbers are: " + str(operands.num1) + ", " + str(operands.num2))
    result = Float32()
    result.data = operands.num1 + operands.num2
    pub.publish(result)

if __name__ == '__main__':
    rospy.init_node('repub_node', anonymous=True)
    rospy.Subscriber("numbers", operands, callback)
    rospy.spin()
