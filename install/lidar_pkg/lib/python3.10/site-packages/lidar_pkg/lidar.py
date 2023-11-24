import rclpy
# import the ROS2 python libraries
from rclpy.node import Node
# import the Twist module from geometry_msgs interface
from geometry_msgs.msg import Twist
# import the LaserScan module from sensor_msgs interface
from sensor_msgs.msg import LaserScan
from rclpy.qos import ReliabilityPolicy, QoSProfile

class  Lidar(Node):

    def __init__(self):

        super().__init__('lidar')
    
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10) # create the publisher object
        # create the subscriber object
        self.subscriber = self.create_subscription(LaserScan, '/scan', self.laser_callback, QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE))
        self.timer_period = 0.5 # define the timer period for 0.5 seconds
        self.laser_forward = 0 # define the variable to save the received info
        
        # create a Twist message
        self.cmd = Twist() 
        self.timer = self.create_timer(self.timer_period, self.motion)

        # define the variables to save the received info
        self.laser_forward = 0
        self.laser_frontLeft = 0
        self.laser_frontRight = 0


    def laser_callback(self,msg):
        # Save the frontal laser scan info at 0°
        self.laser_forward = msg.ranges[359] 
        self.laser_frontLeft = min(msg.ranges[0:15])
        self.laser_frontRight = min(msg.ranges[345:359])
        
    def motion(self):
        # print the data
        self.get_logger().info('I receive: "%s"' % str(self.laser_forward))
        
        if self.laser_frontLeft < 0.5:
            self.get_logger().info('Object front left: "%s"' % str(self.laser_frontLeft))
        if self.laser_frontRight < 0.5:
            self.get_logger().info('Object front right: "%s"' % str(self.laser_frontRight))

        # Logic of movement
        self.cmd.linear.x = 0.0
        self.cmd.angular.z = 0.1
        # Publishing the cmd_vel values to a Topic
        self.publisher_.publish(self.cmd)

            
def main(args=None):

    rclpy.init(args=args)  # initialize the ROS communication
    lidar = Lidar()       # declare the node constructor
    rclpy.spin(lidar)  # pause the program execution, waits for a request to kill the node (ctrl+c)
    lidar.destroy_node()  # Explicity destroy the node
    rclpy.shutdown()    # shutdown the ROS communication

if __name__ == '__main__':
    main()