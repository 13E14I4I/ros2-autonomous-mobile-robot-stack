from math import atan2, asin, sqrt
from math import sin
from math import cos

M_PI=3.1415926535

class Logger:
    
    def __init__(self, filename, headers=["e", "e_dot", "e_int", "stamp"]):
        
        self.filename = filename

        with open(self.filename, 'w') as file:
            
            header_str=""

            for header in headers:
                header_str+=header
                header_str+=", "
            
            header_str+="\n"
            
            file.write(header_str)


    def log_values(self, values_list):

        with open(self.filename, 'a') as file:
            
            vals_str=""
            
            for value in values_list:
                vals_str+=f"{value}, "
            
            vals_str+="\n"
            
            file.write(vals_str)
            

    def save_log(self):
        pass

class FileReader:
    def __init__(self, filename):
        
        self.filename = filename
        
        
    def read_file(self):
        
        read_headers=False

        table=[]
        headers=[]
        with open(self.filename, 'r') as file:

            if not read_headers:
                for line in file:
                    values=line.strip().split(',')

                    for val in values:
                        if val=='':
                            break
                        headers.append(val.strip())

                    read_headers=True
                    break
            
            next(file)
            
            # Read each line and extract values
            for line in file:
                values = line.strip().split(',')
                
                row=[]                
                
                for val in values:
                    if val=='':
                        break
                    row.append(float(val.strip()))

                table.append(row)
        
        return headers, table
    
    

# Implementation Note: Converts quaternion to Euler angles.
def euler_from_quaternion(quat):
    """
    Convert quaternion (w in last place) to euler roll, pitch, yaw.
    quat = [x, y, z, w]
    Returns: yaw (rotation around Z-axis)
    """
    x, y, z, w = quat

    # Compute Euler angles
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    yaw = atan2(siny_cosp, cosy_cosp)  # Extract yaw angle
    # just unpack yaw
    return yaw

# Implementation Note: Calculates Euclidean distance as linear error.
def calculate_linear_error(current_pose, goal_pose):
        
    # Computes linear error in position.
    # current_pose: [x, y, theta, timestamp]; goal_pose: [x, y]
    # Uses Euclidean distance for error calculation.
    
    current_x, current_y, _, _ = current_pose
    goal_x = float(goal_pose[0])
    goal_y = float(goal_pose[1])
    error_linear = sqrt((goal_x - current_x) ** 2 + (goal_y - current_y) ** 2)

    return error_linear

# Implementation Note: Computes angular error between current and desired heading.
def calculate_angular_error(current_pose, goal_pose):

    # Computes angular error in orientation.
    # current_pose: [x, y, theta, timestamp]; goal_pose: [x, y]
    # Uses atan2 to determine desired orientation.
    # Returns the orientation difference between current facing and required heading to reach goal.

    current_x, current_y, current_th, _ = current_pose
    goal_x, goal_y = goal_pose[0],goal_pose[1]

    # Compute desired heading using atan2
    desired_angle = atan2(goal_y - current_y, goal_x - current_x)

    # Compute angular error
    error_angular = desired_angle - current_th

    # Normalize angular error to [-π, π] range.
    error_angular = (error_angular + M_PI) % (2 * M_PI) - M_PI

    
    return error_angular
