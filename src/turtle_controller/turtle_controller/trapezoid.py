#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class Trapezoid(Node):
    def __init__(self):
        super().__init__("Trapezoid")
        self.get_logger().info("Trapezoid node is running")
        self.cmd_vel_pub_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 7)
        self.pose_sub_ = self.create_subscription(Pose, "/turtle1/pose", self.callback, 7)

        
        self.corners = [(9.0, 5.54), (7.0, 8.5),(4.0, 8.5),(3.0, 5.54)]
        self.target_idx = 0

    def callback(self, pose: Pose):
        target_x, target_y = self.corners[self.target_idx]
        msg = Twist()

        dx = target_x - pose.x
        dy = target_y - pose.y
        distance = math.hypot(dx, dy)
        target_theta = math.atan2(dy, dx)
        angle_diff = math.atan2(math.sin(target_theta - pose.theta), math.cos(target_theta - pose.theta))
        if distance < 0.1:
            self.target_idx = (self.target_idx + 1) % len(self.corners)
            return
        if abs(angle_diff) > 0.05:
            msg.angular.z = 2.0 if angle_diff > 0 else -2.0
        else:
            msg.linear.x = 2.0

        self.cmd_vel_pub_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = Trapezoid()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()