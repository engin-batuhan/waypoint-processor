#!/usr/bin/env python
# coding:utf-8
import rospy
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker

def callback(msg):
    global waypoint_filename, marker_pub, idx

    # Record the waypoint
    try:
        with open(waypoint_filename, 'a+') as record_file:
            wp = ",".join(str(i) for i in [msg.pose.position.x, \
                                           msg.pose.position.y, \
                                           msg.pose.position.z, \
                                           msg.pose.orientation.x, \
                                           msg.pose.orientation.y, \
                                           msg.pose.orientation.z, \
                                           msg.pose.orientation.w])
            record_file.write(wp + "\n")
    except Exception as e:
        rospy.logerr("Error while writing to file: {}".format(e))

    # Marker generation
    marker = Marker()
    marker.header.frame_id = "world"
    marker.header.stamp = rospy.Time.now()
    marker.id = idx
    idx += 1
    marker.type = Marker.CYLINDER
    marker.action = Marker.ADD
    marker.pose.position.x = msg.pose.position.x
    marker.pose.position.y = msg.pose.position.y
    marker.pose.position.z = msg.pose.position.z
    marker.scale.x = 1
    marker.scale.y = 1
    marker.scale.z = 1
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0
    marker.color.a = 1.0
    marker.color.r = 1.0
    marker.color.g = 0.0
    marker.color.b = 1.0
    marker_pub.publish(marker)


def waypoint_recorder(sub="/current_pose", file_name='./waypoints.txt'):
    """
    Parameters:
        sub: the geometry_msgs::PoseStamped topic to subscribe
        file_name: the name of the waypoints record
    """
    global waypoint_filename, marker_pub, idx

    waypoint_filename = file_name
    idx = 0

    rospy.init_node('waypoint_recorder', anonymous=True)
    rospy.loginfo("Ready to record the waypoints......")

    marker_pub = rospy.Publisher('/robot_path', Marker, queue_size=10)
    rospy.Subscriber(sub, PoseStamped, callback)

    rospy.spin()

if __name__ == '__main__':
    waypoint_recorder(sub="/current_pose", file_name='./waypoints.txt')
