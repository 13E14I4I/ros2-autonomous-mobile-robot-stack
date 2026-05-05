import sys

from utilities import Logger, euler_from_quaternion
from rclpy.time import Time
from rclpy.node import Node

from rclpy.qos import QoSProfile
from nav_msgs.msg import Odometry as odom

from rclpy import init, spin, shutdown

rawSensor = 0
class localization(Node):
    
    def __init__(self, localizationType=rawSensor):

        super().__init__("localizer")
        
        # Implementation Note: QoS profile for odometry subscription, configured for simulation or real robot.
        # QoS settings based on "ros2 topic info /odom --verbose" as per Tutorial 3.

        odom_qos=QoSProfile(
            reliability=2,  # RELIABLE
            durability=2,  # TRANSIENT_LOCAL
            history=1,  # KEEP_LAST
            depth=10
        )
        #lab 1
        
        self.loc_logger=Logger("robot_pose.csv", ["x", "y", "theta", "stamp"])
        self.pose=None
        
        if localizationType == rawSensor:
        # Implementation Note: Subscribes to odometry topic for pose data.
            self.create_subscription(odom, "/odom", self.odom_callback, odom_qos)
        else:
            print("This type doesn't exist", sys.stderr)
    
    
    def odom_callback(self, pose_msg):
        
        # Implementation Note: Extracts position, orientation, and timestamp from odometry message.
        stamp = pose_msg.header.stamp # Extract timestamp
        x = pose_msg.pose.pose.position.x # Extract position x
        y = pose_msg.pose.pose.position.y # Extract position y
        odom_orientation = pose_msg.pose.pose.orientation # Extract orientation (Quaternion)
        th = euler_from_quaternion([odom_orientation.x, odom_orientation.y, odom_orientation.z, odom_orientation.w])
        
        # Store pose
        self.pose=[x, y, th, stamp]
        
        # Log the data
        self.loc_logger.log_values([self.pose[0], self.pose[1], self.pose[2], Time.from_msg(self.pose[3]).nanoseconds])
    
    def getPose(self):
        return self.pose

# Implementation Note: Main guard to run localization node when executed as script.
if __name__=="__main__":
    init()  # Initialize ROS2

    node = localization()  # Instantiate the localization node

    try:
        spin(node)  # Run node
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        node.destroy_node()  # Clean up the node
        shutdown()
    