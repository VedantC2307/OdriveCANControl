#include <rclcpp/rclcpp.hpp>
#include <odrive_can/msg/control_message.hpp>
#include <std_msgs/msg/float32.hpp>

using std::placeholders::_1;

class ODrivePublisher : public rclcpp::Node
{
public:
  ODrivePublisher() : Node("odrive_publisher"), control_torque_(0.0)
  {
    control_data_subscription_ = this->create_subscription<std_msgs::msg::Float32>(
      "/odrive_axis0/control_data", 10, std::bind(&ODrivePublisher::control_data_callback, this, _1));

    control_message_publisher_ = this->create_publisher<odrive_can::msg::ControlMessage>(
      "/odrive_axis0/control_message", 10);

    // Create a timer to call publish_control_message at 10Hz
    timer_ = this->create_wall_timer(
      std::chrono::milliseconds(10), std::bind(&ODrivePublisher::publish_control_message, this));
  }

private:
  void control_data_callback(const std_msgs::msg::Float32::SharedPtr msg)
  {
    control_torque_ = msg->data;
    RCLCPP_INFO(this->get_logger(), "Implementing Control Callback: %f", control_torque_);
  }

  void publish_control_message()
  {
    try
    {
      auto control_msg = odrive_can::msg::ControlMessage();
      control_msg.control_mode = 2;
      control_msg.input_mode = 1;
      control_msg.input_pos = 0.0;
      control_msg.input_vel = 0.2;
      control_msg.input_torque = 0.0;

      control_message_publisher_->publish(control_msg);

      RCLCPP_INFO(this->get_logger(), "Published control message: control_mode=%d, input_mode=%d, input_pos=%f, input_vel=%f, input_torque=%f",
                  control_msg.control_mode, control_msg.input_mode, control_msg.input_pos, control_msg.input_vel, control_msg.input_torque);
    }
    catch (const std::exception &e)
    {
      RCLCPP_ERROR(this->get_logger(), "Failed to publish control message: %s", e.what());
    }
  }

  rclcpp::Subscription<std_msgs::msg::Float32>::SharedPtr control_data_subscription_;
  rclcpp::Publisher<odrive_can::msg::ControlMessage>::SharedPtr control_message_publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  float control_torque_;
};

int main(int argc, char *argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ODrivePublisher>());
  rclcpp::shutdown();
  return 0;
}
