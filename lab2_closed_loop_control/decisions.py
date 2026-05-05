# Imports


import sys

from utilities import euler_from_quaternion, calculate_angular_error, calculate_linear_error
from pid import PID_ctrl

from rclpy import init, spin, spin_once
from rclpy.node import Node
from geometry_msgs.msg import Twist

from rclpy.qos import QoSProfile
from nav_msgs.msg import Odometry as odom

from localization import localization, rawSensor

from planner import TRAJECTORY_PLANNER, POINT_PLANNER, planner
from controller import controller, trajectoryController

# You may add any other imports you may need/want to use below
# import ...


class decision_maker(Node):
    
    def __init__(self, publisher_msg, publishing_topic, qos_publisher, goalPoint, rate=10, motion_type=POINT_PLANNER):

        super().__init__("decision_maker")

        # Implementation Note: Publisher for sending velocity commands to control robot motion.
        self.vel_publisher= self.create_publisher(publisher_msg, publishing_topic, qos_publisher)

        publishing_period=1/rate
        
        # Implementation Note: Controller instantiation with tuned PID parameters for the selected planner type.
        if motion_type == POINT_PLANNER:
            self.controller=controller(klp=.5, klv=0.2, kli= 0.01, kap=0.8, kav=0.6, kai=0.1)
            self.planner=planner(POINT_PLANNER)    
    
    
        elif motion_type==TRAJECTORY_PLANNER:
            self.controller=trajectoryController(klp=.5, klv=0.2, kli= 0.01, kap=0.8, kav=0.6, kai=0.1)
            self.planner=planner(TRAJECTORY_PLANNER)

        else:
            print("Error: unsupported planner type", file=sys.stderr)

        # Instantiate the localization, use rawSensor for now  
        self.localizer=localization(rawSensor)

        # Instantiate the planner
        # goalPoint parameter applies only to point planner.
        self.goal=self.planner.plan(goalPoint)

        self.create_timer(publishing_period, self.timerCallback)


    def timerCallback(self):
        
        # Implementation Note: Executes localization update to get current pose.
        spin_once(self.localizer) # This file runs the decision_maker node concurrently.
        #rint("test")
        if self.localizer.getPose()  is  None:
            print("waiting for odom msgs ....")
            return

        vel_msg=Twist()
        
        # Implementation Note: Checks if the robot has reached the goal based on linear error threshold.
        if type(self.goal) == list:
            e_threashold = 0.5
            error = calculate_linear_error(self.localizer.getPose(),self.goal[-1])
            if(error < e_threashold):
                reached_goal=True
            else:
                reached_goal=False
                
            
        else: 
            reached_goal=False
        

        if reached_goal:
            print("reached goal")
            self.publisher.publish(vel_msg)
            
            self.controller.PID_angular.logger.save_log()
            self.controller.PID_linear.logger.save_log()
            
            # Implementation Note: Terminates the node execution upon reaching the goal.
            raise SystemExit #something to do with SystemExit
        
        velocity, yaw_rate = self.controller.vel_request(self.localizer.getPose(), self.goal, True)
        print(velocity)
        print(yaw_rate)
        # Implementation Note: Publishes computed velocity commands to the robot.
        #vel_msg = Twist()
        vel_msg.linear.x=velocity
        vel_msg.angular.z=yaw_rate

        self.vel_publisher.publish(vel_msg)

import argparse


def main(args=None):
    
    init()

    # Implementation Note: QoS profile configured for odometry topic, adaptable for simulation or real robot.
    # QoS settings based on "ros2 topic info /odom --verbose" as per Tutorial 3.
    odom_qos=QoSProfile(reliability=2, durability=2, history=1, depth=10)
    

    # Implementation Note: Instantiates decision maker with appropriate parameters based on motion type.
    if args.motion.lower() == "point":
        DM=decision_maker(publisher_msg=Twist, publishing_topic="/cmd_vel", qos_publisher=10, goalPoint=[-1.0, 1.0], motion_type=POINT_PLANNER)
    elif args.motion.lower() == "trajectory":
        DM=decision_maker(publisher_msg=Twist, publishing_topic="/cmd_vel", qos_publisher=10, goalPoint=[1.0, 1.0], motion_type=TRAJECTORY_PLANNER)
    else:
        print("invalid motion type", file=sys.stderr)        
    
    
    
    try:
        spin(DM)
    except SystemExit:
        print(f"reached there successfully {DM.localizer.pose}")


if __name__=="__main__":

    argParser=argparse.ArgumentParser(description="point or trajectory") 
    argParser.add_argument("--motion", type=str, default="point")
    args = argParser.parse_args()

    main(args)
