# Lab 3 — Localization (Particle Filter)

## Purpose

This module implements probabilistic localization for a mobile robot using a particle filter.

It estimates the robot’s pose in a mapped environment by combining:
- motion models
- LiDAR sensor measurements
- occupancy grid maps

## Implemented Functionality

- Implemented particle filter for pose estimation
- Developed motion model for particle propagation
- Constructed likelihood field from occupancy maps
- Computed particle weights based on LiDAR observations
- Performed resampling to improve state distribution
- Tuned sensor noise parameters for improved localization accuracy
- Visualized particle convergence and pose estimation in RViz

## Key Files

- `particleFilter.py` — main particle filter execution loop
- `particle.py` — particle representation, motion model, and weight computation
- `mapUtilities.py` — likelihood field generation and map processing
- `localization.py` — integrates particle filter into system pipeline
- `decisions.py` — connects localization with control and planning modules
- `planner.py` — provides goal positions for navigation
- `controller.py` — executes motion commands based on estimated pose

## Role in Full Stack

This module replaces raw odometry with probabilistic state estimation, enabling accurate localization in the presence of sensor noise and drift.

It is a critical component for reliable path planning and autonomous navigation in Lab 4.
