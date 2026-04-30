# Lab 2 — Closed-Loop Control

## Purpose

This module implements closed-loop control for a TurtleBot4 mobile robot using position feedback from odometry.

It focuses on:
- point-to-point control
- trajectory tracking
- P, PI, PD, and PID control
- gain tuning and performance comparison
- logging tracking errors for post-run analysis

## Implemented Functionality

- Built a controller pipeline using odometry feedback
- Computed linear and angular tracking errors
- Implemented P, PI, PD, and PID control laws
- Added velocity saturation limits for safe robot motion
- Generated point, parabola, and sigmoid trajectory references
- Tuned controller gains based on tracking accuracy, overshoot, and response speed
- Logged pose and error data for visualization and comparison

## Key Files

- `pid.py` — implements P/PI/PD/PID control logic, error tracking, and logging
- `controller.py` — converts controller output into velocity commands with saturation limits
- `planner.py` — generates point and trajectory references
- `localization.py` — reads odometry-based robot pose
- `decisions.py` — coordinates localization, planning, control, and command publishing
- `plot_errors.py` — visualizes logged pose/error data
- `utilities.py` — helper functions for error calculation and pose handling

## Role in Full Stack

This module provides the feedback-control layer used later by the particle-filter localization and A* path-planning modules.

It establishes the ability to convert robot pose error into motion commands, allowing the robot to follow points and trajectories before full autonomous navigation is introduced.
