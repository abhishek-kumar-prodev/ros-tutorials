#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import time
from my_robot_interfaces.srv import SetLed

class BatteryClientNode(Node):
    def __init__(self):
        super().__init__("battery_client")
        self.client_ = self.create_client(SetLed, "set_led")

    def call_set_led_client(self, led_number:int, led_state:bool):
        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for the set led service...")

        request = SetLed.Request()
        request.led_number = led_number
        request.led_state = led_state

        future = self.client_.call_async(request)
        future.add_done_callback(self.callback_call_led_client)

    def callback_call_led_client(self, future):
        response = future.result()
        self.get_logger().info("Request Completed::-> "+ str(response.success))


def main(args=None):
    rclpy.init(args=args)
    node = BatteryClientNode()
    while 1:
        node.call_set_led_client(3,True)
        time.sleep(4)
        node.call_set_led_client(3,False)
        time.sleep(6)
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
