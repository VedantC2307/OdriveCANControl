#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/float32.hpp>
#include <odrive_can/msg/control_message.hpp>
#include <odrive_can/msg/controller_status.hpp>

using std::placeholders::_1;

class ODriveControl : public rclcpp::Node
{
public:
  ODriveControl() : Node("odrive_control")
  {
    RCLCPP_INFO(this->get_logger(), "Starting node");

    subscription_ = this->create_subscription<odrive_can::msg::ControllerStatus>(
      "/odrive_axis0/controller_status", 10, std::bind(&ODriveControl::control_callback, this, _1));

    publisher_ = this->create_publisher<odrive_can::msg::ControlMessage>(
      "/odrive_axis0/control_message", 10);
  }

private:
  void control_callback(const odrive_can::msg::ControllerStatus::SharedPtr msg)
  {
    RCLCPP_INFO(this->get_logger(), "Implementing Control Callback");

    try
    {
      float position_value = msg->vel_estimate;

      // Callback function to implement impedance controller
      impedance_control_logic_callback(position_value);
    }
    catch (const std::exception &e)
    {
      RCLCPP_ERROR(this->get_logger(), "Message attribute error: %s", e.what());
    }
  }

  void impedance_control_logic_callback(float position_value)
  {
    RCLCPP_INFO(this->get_logger(), "Implementing Control logic loop");

    float position = position_value;
    RCLCPP_INFO(this->get_logger(), "Received: %f", position);

    float torque = 0.0;

    // Send Torque message
    auto create_msg = odrive_can::msg::ControlMessage();
    create_msg.control_mode = 2;  // Torque = 1, Velocity = 2 Position = 3
    create_msg.input_mode = 1;    // Passthrough = 1
    create_msg.input_pos = 0.0;
    create_msg.input_vel = 0.2;
    create_msg.input_torque = torque;

    RCLCPP_INFO(this->get_logger(), "Publishing: control_mode=%d, input_mode=%d, input_pos=%f, input_vel=%f, input_torque=%f",
                create_msg.control_mode, create_msg.input_mode, create_msg.input_pos, create_msg.input_vel, create_msg.input_torque);

    publisher_->publish(create_msg);
  }

  rclcpp::Subscription<odrive_can::msg::ControllerStatus>::SharedPtr subscription_;
  rclcpp::Publisher<odrive_can::msg::ControlMessage>::SharedPtr publisher_;
};

int main(int argc, char *argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ODriveControl>());
  rclcpp::shutdown();
  return 0;
}
