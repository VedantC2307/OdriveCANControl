// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_msgs:msg/FrictionComp.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__MSG__DETAIL__FRICTION_COMP__BUILDER_HPP_
#define CUSTOM_MSGS__MSG__DETAIL__FRICTION_COMP__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_msgs/msg/detail/friction_comp__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_msgs
{

namespace msg
{

namespace builder
{

class Init_FrictionComp_tau_fcomp
{
public:
  Init_FrictionComp_tau_fcomp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_msgs::msg::FrictionComp tau_fcomp(::custom_msgs::msg::FrictionComp::_tau_fcomp_type arg)
  {
    msg_.tau_fcomp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::msg::FrictionComp msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::msg::FrictionComp>()
{
  return custom_msgs::msg::builder::Init_FrictionComp_tau_fcomp();
}

}  // namespace custom_msgs

#endif  // CUSTOM_MSGS__MSG__DETAIL__FRICTION_COMP__BUILDER_HPP_
