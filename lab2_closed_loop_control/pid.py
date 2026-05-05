from rclpy.time import Time
from utilities import Logger

# Controller type
P=0 # proportional
PD=1 # proportional and derivative
PI=2 # proportional and integral
PID=3 # proportional, integral, derivative

class PID_ctrl:
    
    def __init__(self, type_, kp=1,kv=0.8,ki=0.2, history_length=3, filename_="errors.csv"):
        
        # Data for the controller
        self.history_length=history_length
        self.history=[]
        self.type=type_

        # Controller gains
        self.kp=kp    # proportional gain
        self.kv=kv    # derivative gain
        self.ki=ki    # integral gain
        
        self.logger=Logger(filename_,headers=["e", "e_dot", "e_int", "stamp"])
        # Logs error, error_dot, error_int, and timestamp to the specified file.

    
    def update(self, stamped_error, status):
        
        if status == False:
            self.__update(stamped_error)
            return 0.0
        else:
            return self.__update(stamped_error)

        
    def __update(self, stamped_error):
        
        latest_error=stamped_error[0]
        stamp=stamped_error[1]
        
        self.history.append(stamped_error)        
        
        if (len(self.history) > self.history_length):
            self.history.pop(0)
        
        # If insufficient data points, use only the proportional gain
        if (len(self.history) != self.history_length):
            return self.kp * latest_error
        
        # Compute the error derivative
        dt_avg=0
        error_dot=0
        
        for i in range(1, len(self.history)):
            
            t0=Time.from_msg(self.history[i-1][1])
            t1=Time.from_msg(self.history[i][1])
            
            dt=(t1.nanoseconds - t0.nanoseconds) / 1e9
            
            dt_avg+=dt



            # use constant dt if the messages arrived inconsistent
            # for example dt=0.1 overwriting the calculation          
            
            # Implementation Note: Computes the derivative of the error over time.
            #error_dot += (self.history[len(self.history)][0]-self.history[len(self.history)-1][0])/dt
            error_dot += (self.history[i][0]-self.history[i-1][0])/dt
            #error_dot = 0
        
        #total_l = len(self.history)
        #error_dot = self.history[total_l][0] - self.history[total_l - 1][0]    
        error_dot/=len(self.history)
        dt_avg/=len(self.history)
        
        # Compute the error integral
        sum_=0
        for hist in self.history:
            # Implementation Note: Accumulates error for integral calculation.
            sum_+= hist[0]
            pass
        
        error_int=sum_*dt_avg



        # Implementation Note: Logs error components and timestamp.
        self.logger.log_values([latest_error,error_dot,error_int,Time.from_msg(stamp).nanoseconds])
        
        # Implementation Note: Proportional control law.
        if self.type == P:
            return self.kp * latest_error
        
        # Implementation Note: Control laws for PD, PI, and PID controllers.
        elif self.type == PD:
            pass
            return (self.kp * latest_error + self.kv * error_dot)
        
        elif self.type == PI:
            pass
            return (self.kp * latest_error + self.ki * error_int) 
        
        elif self.type == PID:
            pass
            return (self.kp * latest_error + self.ki * error_int + self.kv * error_dot)
