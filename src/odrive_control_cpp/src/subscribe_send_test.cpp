#include <rclcpp/rclcpp.hpp>
#include <odrive_can/msg/controller_status.hpp>
#include <std_msgs/msg/float32.hpp>

using std::placeholders::_1;

class ODriveControl : public rclcpp::Node
{
public:
  ODriveControl() : Node("odrive_control")
  {
    subscription_ = this->create_subscription<odrive_can::msg::ControllerStatus>(
      "/odrive_axis0/controller_status", 50, std::bind(&ODriveControl::control_callback, this, _1));

    control_data_publisher_ = this->create_publisher<std_msgs::msg::Float32>(
      "/odrive_axis0/control_data", 50);
  }

private:
  void control_callback(const odrive_can::msg::ControllerStatus::SharedPtr msg)
  {
    RCLCPP_INFO(this->get_logger(), "Implementing Control Callback");

    float velocity_value = msg->vel_estimate;
    impedance_control_logic_callback(velocity_value);
  }

  void impedance_control_logic_callback(float velocity_value)
  {
    RCLCPP_INFO(this->get_logger(), "Implementing Control logic loop");

    float position = velocity_value;
    // float control_output = 0.0;  // Example control logic

    std_msgs::msg::Float32 control_msg;
    control_msg.data = position;

    control_data_publisher_->publish(control_msg);
  }

  rclcpp::Subscription<odrive_can::msg::ControllerStatus>::SharedPtr subscription_;
  rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr control_data_publisher_;
};

int main(int argc, char *argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ODriveControl>());
  rclcpp::shutdown();
  return 0;
}
