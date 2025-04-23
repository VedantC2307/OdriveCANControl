// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_msgs:msg/MotionState.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__MSG__DETAIL__MOTION_STATE__BUILDER_HPP_
#define CUSTOM_MSGS__MSG__DETAIL__MOTION_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_msgs/msg/detail/motion_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_msgs
{

namespace msg
{

namespace builder
{

class Init_MotionState_velocity
{
public:
  explicit Init_MotionState_velocity(::custom_msgs::msg::MotionState & msg)
  : msg_(msg)
  {}
  ::custom_msgs::msg::MotionState velocity(::custom_msgs::msg::MotionState::_velocity_type arg)
  {
    msg_.velocity = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::msg::MotionState msg_;
};

class Init_MotionState_position
{
public:
  Init_MotionState_position()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MotionState_velocity position(::custom_msgs::msg::MotionState::_position_type arg)
  {
    msg_.position = std::move(arg);
    return Init_MotionState_velocity(msg_);
  }

private:
  ::custom_msgs::msg::MotionState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::msg::MotionState>()
{
  return custom_msgs::msg::builder::Init_MotionState_position();
}

}  // namespace custom_msgs

#endif  // CUSTOM_MSGS__MSG__DETAIL__MOTION_STATE__BUILDER_HPP_
