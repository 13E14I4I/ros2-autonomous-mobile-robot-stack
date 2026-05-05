# Type of planner
POINT_PLANNER=0; TRAJECTORY_PLANNER=1



class planner:
    def __init__(self, type_):

        self.type=type_

    
    def plan(self, goalPoint=[-1.0, -1.0]):
        
        if self.type==POINT_PLANNER:
            return self.point_planner(goalPoint)
        
        elif self.type==TRAJECTORY_PLANNER:
            return self.trajectory_planner()


    def point_planner(self, goalPoint):
        x = goalPoint[0]
        y = goalPoint[1]
        return x, y

    # Implementation Note: Generates trajectory points for predefined paths.
    def trajectory_planner(self):
        from math import exp

        """
        Generates trajectory points for Parabola and Sigmoid paths.
        Returns a list of [x, y] coordinates.
        The two trajectory equations are given in the lab manual 
        """
        trajectory_points = []


        # Generate points for Parabola (y = x^2, x in [0.0, 1.5])
        for x in [i * 0.1 for i in range(16)]:  # Generates x = 0.0, 0.1, ..., 1.5
            y = x**2
            trajectory_points.append([x, y])
            print(trajectory_points)
        
        # # Generate points for Sigmoid (y = 2/(1+e^-2x) - 1, x in [0.0, 2.5])
        # for x in [i * 0.1 for i in range(26)]:  # Generates x = 0.0, 0.1, ..., 2.5
        #     y = 2 / (1 + exp(-2 * x)) - 1
        #     trajectory_points.append([x, y])

        return trajectory_points  # the return is a list of trajectory points: [ [x1,y1], ..., [xn,yn]]

