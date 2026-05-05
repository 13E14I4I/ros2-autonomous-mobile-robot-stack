# ROS2 Autonomous Mobile Robot Navigation Stack

## Overview

This project implements a full autonomous mobile robotics pipeline using ROS2 and TurtleBot4, integrating perception, localization, planning, and control into a complete navigation system.

The system enables a robot to:
- Process real-time sensor data (IMU, LiDAR, odometry)
- Estimate its pose using particle filter localization
- Generate collision-free paths using A* planning
- Execute trajectories using closed-loop PID control

The final system performs end-to-end autonomous navigation from goal selection to execution.


## Acknowledgement

This project was developed as part of ME597 (Autonomous Mobile Robots) at the University of Waterloo in a team of four.

Original course/lab materials:
- ME597c student repository: https://github.com/ntntran200701/ME597c-Students
- MTE544 student repository: https://github.com/UW-MTE544/MTE544_student

For each major module, each team member independently developed or attempted implementations, then we reviewed, tested, and compared each solution as a group. The final repository reflects the implementations that worked best after collaborative debugging and validation.

## System Architecture

**Sensor Data → Localization → Planning → Control → Actuation**

- Sensor data (IMU, LiDAR, odometry) is processed in real time
- Particle filter estimates robot pose
- A* planner generates optimal paths
- PID controller tracks trajectory
- Commands are executed on the robot

<p align="center">
  <img src=overview.jpg>
</p>


## Modules

### [Sensor Data Processing](./lab1_sensor_processing)
ROS2-based sensor acquisition, motion primitives, and data logging.

### [Closed-Loop Control](./lab2_closed_loop_control)
P/PI/PD/PID controllers for trajectory tracking and error minimization.

### [Localization (Particle Filter)](./lab3_particle_filter_localization)
Probabilistic pose estimation using LiDAR and occupancy maps.

### [Path Planning and Navigation](./lab4_path_planning_navigation)
A* path planning integrated with localization and control for full autonomy.


## Key Technologies

- ROS2  
- Python  
- TurtleBot4  
- RViz  
- LiDAR / IMU / Odometry  
- PID Control  
- Particle Filter  
- A* Path Planning
