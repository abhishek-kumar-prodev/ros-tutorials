#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import LedPanelState
from my_robot_interfaces.srv import SetLed
from functools import partial

class LedPanelServerNode(Node):
    def __init__(self):
        super().__init__("led_panel_server")

        self.declare_parameter("led_states", [0,0,0])
        led_states_ = self.get_parameter("led_states").value

        self.led_panel_state = LedPanelState(led_state=led_states_)
        self.pub_ = self.create_publisher(
            LedPanelState, "led_panel_state", 10)
        self.set_led_service_ = self.create_service(
            SetLed, "set_led", self.callback_set_led)
        self.timer_ = self.create_timer(5, self.publish_led_state)
        self.get_logger().info("LED Panel Server has been started...")

    def publish_led_state(self):
        msg = self.led_panel_state
        self.pub_.publish(msg)

    def callback_set_led(self, request: SetLed.Request, response: SetLed.Response):
        if not (1 <= request.led_number <= 3):
            response.success = False
            self.get_logger().warn(f"Invalid LED number: {request.led_number}")
            return response

        self.led_panel_state.led_state[request.led_number - 1] = int(request.led_state)
        response.success = True
        self.publish_led_state()
        return response
        

def main(args=None):
    rclpy.init(args=args)
    node = LedPanelServerNode() 
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
