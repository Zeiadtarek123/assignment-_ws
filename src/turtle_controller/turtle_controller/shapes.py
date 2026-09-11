#!/usr/bin/env python3
import rclpy
import threading
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import TeleportAbsolute
from turtle_interfaces.srv import SelectShape
import math


class Shapes(Node):
    def __init__(self):
        super().__init__("shapes")
        self.get_logger().info("shapes node is running")
        self.counter = 0
        self.shape_name = "pause"  

        self.cmd_vel_pub_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 7)
        self.pose_sub_ = self.create_subscription(Pose, "/turtle1/pose", self.callback, 7)
        #the cleint that will return trtle to midpoint
        self.teleport_client = self.create_client(TeleportAbsolute, "/turtle1/teleport_absolute")
        #the costum service waiting for user input
        self.srv = self.create_service(SelectShape, "/select_shape", self.service_callback)
        #the thread thng to get the puase and reset option done
        self.input_thread = threading.Thread(target=self.ask_for_shape_name, daemon=True)
        self.input_thread.start()

        self.shapes = {
            "triangle": [(8.0, 5.54), (5.54, 9.0), (3.0, 5.54)],
            "parallelogram": [(9.0, 5.54), (10.0, 8.5), (6.0, 8.5), (5.0, 5.54)],
            "trapezoid": [(9.0, 5.54), (7.0, 8.5), (4.0, 8.5), (3.0, 5.54)]
        } #customizable but those are MY good points
        self.target_idx = 0

        

    def process_command(self, user_input: str) -> tuple[bool, str]:
        valid_options = ["triangle", "parallelogram", "trapezoid", "pause", "reset"]
        if user_input in valid_options:
            if user_input in self.shapes and user_input != self.shape_name:
                self.target_idx = 0 
            self.shape_name = user_input
            return True, f"Command '{user_input}' executed successfully."
        else:
            return False, f"Invalid input '{user_input}'! Valid options: {valid_options}"

    def service_callback(self, request, response):
        cmd = request.shape_name.strip().lower()
        success, message = self.process_command(cmd)
        response.success = success
        response.message = message
        return response

    def ask_for_shape_name(self):
        while rclpy.ok():
            user_input = input("Please enter shape name: [triangle, parallelogram, trapezoid, pause, reset]:\n").strip().lower()
            success, message = self.process_command(user_input)
            if not success:
                print("Invalid input! Please enter the proper form asked.")

    def follow_waypoints(self, pose: Pose) -> Twist:
        msg = Twist()
        active_corners = self.shapes[self.shape_name]
        target_x, target_y = active_corners[self.target_idx]

        dx = target_x - pose.x
        dy = target_y - pose.y
        distance = math.hypot(dx, dy)
        target_theta = math.atan2(dy, dx)
        angle_diff = math.atan2(math.sin(target_theta - pose.theta), math.cos(target_theta - pose.theta)) 

        if distance < 0.1: 
            self.target_idx = (self.target_idx + 1) % len(active_corners) #this smart af
            return msg 

        if abs(angle_diff) > 0.05: 
            if angle_diff > 0:
                msg.angular.z = 2.0
            else:
                msg.angular.z = -2.0
        else: 
            msg.linear.x = 2.0

        return msg

    def callback(self, pose: Pose):
        msg = Twist()
        match self.shape_name:
            case "triangle" | "parallelogram" | "trapezoid":
                msg = self.follow_waypoints(pose) 

            case "pause":
                self.cmd_vel_pub_.publish(Twist())
                return

            case "reset":
                req = TeleportAbsolute.Request()
                req.x = 5.54
                req.y = 5.54
                req.theta = 0.0
                self.teleport_client.call_async(req)
                
                #i figured i have to stop moving after reseting so...
                self.shape_name = "pause"
                self.cmd_vel_pub_.publish(Twist())
                return #after each publish(inside switchcase) we must get out of callback

            case _:
                return

        self.cmd_vel_pub_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = Shapes()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()