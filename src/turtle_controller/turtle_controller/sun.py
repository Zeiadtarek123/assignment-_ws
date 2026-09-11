#!/usr/bin/env python3

#JUST BY TRAIL AND ERROR AND IT FELT COOL SO ... 

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
class Triangle(Node):
   
    def __init__(self): # methode
        super().__init__("triangle")
        self.get_logger().info("triangle node is running")
        self.cmd_vel_pub_=self.create_publisher(Twist,"/turtle1/cmd_vel",11)
        self.counter=0
        self.timer_= self.create_timer(2.0,self.draw_triangle_callback)

    def draw_triangle_callback(self):
        msg = Twist()
        if self.counter ==0:
            msg.linear.x=2.0
            self.counter += 1
        elif self.counter ==1:
            msg.angular.z=2.2
            self.counter-=1
       
        self.cmd_vel_pub_.publish(msg)


    

def main(args=None):
    rclpy.init(args=args)
    node = Triangle()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()