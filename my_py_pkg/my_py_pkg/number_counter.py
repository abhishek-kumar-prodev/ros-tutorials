#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool

class NumberCounterNode(Node):
    def __init__(self):
        super().__init__("number_counter") 
        self.counter_ = 0
        self.subscriber_ = self.create_subscription(
            Int64,"number", self.callback_number_counter, 10)
        self.publisher_ = self.create_publisher(Int64, "number_count", 10)
        self.services_  = self.create_service(SetBool, "reset_counter", self.callback_reset_counter)
        
    def callback_number_counter(self, msg:Int64):
        self.counter_ += msg.data
        self.get_logger().info("Number received: " + str(msg.data))
        self.publisher_.publish(msg)
        self.get_logger().info("Counter value: " + str(self.counter_))

    def callback_reset_counter(self, request:SetBool.Request, response:SetBool.Response):
        if request.data==True:
            self.counter_=0
            response.success = True
            response.message = "Counter set to zero"
            self.get_logger().info("Counter has been reset.")
        else:
            response.success = False
            response.message = "No changes to counter"
            self.get_logger().info("No action taken due to no request")
        return response

        


def main(args=None):
    rclpy.init(args=args)
    node = NumberCounterNode() 
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()