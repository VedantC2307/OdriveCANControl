// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_msgs:msg/ImpedanceTorque.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__MSG__DETAIL__IMPEDANCE_TORQUE__BUILDER_HPP_
#define CUSTOM_MSGS__MSG__DETAIL__IMPEDANCE_TORQUE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_msgs/msg/detail/impedance_torque__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_msgs
{

namespace msg
{

namespace builder
{

class Init_ImpedanceTorque_tau_imp
{
public:
  Init_ImpedanceTorque_tau_imp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_msgs::msg::ImpedanceTorque tau_imp(::custom_msgs::msg::ImpedanceTorque::_tau_imp_type arg)
  {
    msg_.tau_imp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::msg::ImpedanceTorque msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::msg::ImpedanceTorque>()
{
  return custom_msgs::msg::builder::Init_ImpedanceTorque_tau_imp();
}

}  // namespace custom_msgs

#endif  // CUSTOM_MSGS__MSG__DETAIL__IMPEDANCE_TORQUE__BUILDER_HPP_
