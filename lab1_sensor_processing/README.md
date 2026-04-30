# Lab 1 — Sensor Data Processing

## Purpose

This module introduces ROS2-based sensor reading, motion command publishing, and data logging for a TurtleBot4 mobile robot.

It focuses on:
- reading IMU, LiDAR, and odometry data
- publishing velocity commands to `/cmd_vel`
- executing basic motion primitives
- logging sensor outputs for analysis and visualization

## Implemented Functionality

- Configured ROS2 publishers and subscribers for robot motion and sensor streams
- Implemented motion primitives:
  - straight-line motion
  - circular motion
  - spiral motion
- Logged IMU, LiDAR, and odometry outputs during robot movement
- Visualized collected sensor data for post-run analysis
- Generated a basic SLAM map for use in later localization and planning modules

## Key Files

- `motions.py` — main robot motion and sensor logging script
- `utilities.py` — helper functions for sensor processing, logging, and coordinate handling
- `filePlotter.py` — plots logged sensor data
- `image_viz.py` — visualizes map/image data, if used

## Role in Full Stack

This module provides the foundation for the later robotics stack by establishing sensor access, robot command publishing, and data logging workflows used in control, localization, and planning.
