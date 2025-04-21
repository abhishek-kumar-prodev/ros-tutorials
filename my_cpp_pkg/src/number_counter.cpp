#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/int64.hpp"

using namespace std::placeholders;

class NumberCounterNode : public rclcpp::Node
{
public:
    NumberCounterNode() : Node("number_counter") , counter_(0)
    {
        subscriber_ = this->create_subscription<example_interfaces::msg::Int64>(
            "number", 10, 
            std::bind(&NumberCounterNode::callbackNumberCounter, this,_1));
        publisher_ = this->create_publisher<example_interfaces::msg::Int64>("number_count",10);
        RCLCPP_INFO(this->get_logger(), "Number counter has started....");

    }

private:
    void callbackNumberCounter(const example_interfaces::msg::Int64::SharedPtr msg)
    {
        RCLCPP_INFO(this->get_logger(),"Number Received: %ld", msg->data);
        counter_ +=msg->data;
        auto newMsg = example_interfaces::msg::Int64();
        newMsg.data = counter_;
        publisher_->publish(newMsg);
        
    }
    rclcpp::Subscription<example_interfaces::msg::Int64>::SharedPtr subscriber_;
    rclcpp::Publisher<example_interfaces::msg::Int64>::SharedPtr publisher_;
    int counter_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<NumberCounterNode>(); 
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
