import rclpy
# import the ROS2 python libraries
from rclpy.node import Node
# import the Twist module from geometry_msgs interface
from geometry_msgs.msg import Twist
# import the LaserScan module from sensor_msgs interface
from sensor_msgs.msg import LaserScan
from rclpy.qos import ReliabilityPolicy, QoSProfile
import random

class  Lidar(Node):

    def __init__(self):
        # Here you have the class constructor
        # call the class constructor
        super().__init__('lidar')
        # create the publisher object
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        # create the subscriber object
        self.subscriber = self.create_subscription(LaserScan, '/scan', self.laser_callback, QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE))
        # define the timer period for 0.5 seconds
        self.timer_period = 0.5
        # define the variable to save the received info
        self.laser_forward = 0
        # create a Twist message
        self.cmd = Twist()
        self.timer = self.create_timer(self.timer_period, self.motion)
        self.counter = 0  # add this line to initialize the counter

    def laser_callback(self,msg):
        # Save the frontal laser scan info at 0°
        self.laser_forward = msg.ranges[359] 
        
        
    

    def motion(self):
        # print the data
        self.get_logger().info('I receive: "%s"' % str(self.laser_forward))
        # Logic of move
        if self.laser_forward < 1.5:  # if obstacle is closer than 1.5m
            self.cmd.linear.x = 0.0  # stop moving forward
            self.cmd.angular.z = 0.5  # start turning
        else:
            self.cmd.linear.x = 0.2  # move forward
            if self.counter % 2 == 0:
                self.cmd.angular.z = 0.1  # turn right
            else:
                self.cmd.angular.z = -0.1  # turn left
            self.counter += 1  # increment the counter
        # Publishing the cmd_vel values to a Topic
        self.publisher_.publish(self.cmd)

    # def motion(self):
    #     # print the data
    #     self.get_logger().info('I receive: "%s"' % str(self.laser_forward))
    #     # Logic of move
    #     if self.laser_forward < 1.5:  # if obstacle is closer than 1.5m
    #         self.cmd.linear.x = 0.0  # stop moving forward
    #         self.cmd.angular.z = random.uniform(0.5, 1.0)  # start turning at a random speed
    #     else:
    #         self.cmd.linear.x = random.uniform(0.1, 0.3)  # move forward at a random speed
    #         self.cmd.angular.z = random.uniform(-0.1, 0.1)  # turn at a random speed
    #     # Publishing the cmd_vel values to a Topic
    #     self.publisher_.publish(self.cmd)
            
def main(args=None):
    # initialize the ROS communication
    rclpy.init(args=args)
    # declare the node constructor
    lidar = Lidar()       
    # pause the program execution, waits for a request to kill the node (ctrl+c)
    rclpy.spin(lidar)
    # Explicity destroy the node
    lidar.destroy_node()
    # shutdown the ROS communication
    rclpy.shutdown()

if __name__ == '__main__':
    main()