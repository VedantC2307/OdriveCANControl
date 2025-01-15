// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_msgs:srv/ODriveCommand.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__SRV__DETAIL__O_DRIVE_COMMAND__BUILDER_HPP_
#define CUSTOM_MSGS__SRV__DETAIL__O_DRIVE_COMMAND__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_msgs/srv/detail/o_drive_command__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_msgs
{

namespace srv
{

namespace builder
{

class Init_ODriveCommand_Request_command
{
public:
  Init_ODriveCommand_Request_command()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_msgs::srv::ODriveCommand_Request command(::custom_msgs::srv::ODriveCommand_Request::_command_type arg)
  {
    msg_.command = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::srv::ODriveCommand_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::srv::ODriveCommand_Request>()
{
  return custom_msgs::srv::builder::Init_ODriveCommand_Request_command();
}

}  // namespace custom_msgs


namespace custom_msgs
{

namespace srv
{

namespace builder
{

class Init_ODriveCommand_Response_message
{
public:
  explicit Init_ODriveCommand_Response_message(::custom_msgs::srv::ODriveCommand_Response & msg)
  : msg_(msg)
  {}
  ::custom_msgs::srv::ODriveCommand_Response message(::custom_msgs::srv::ODriveCommand_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::srv::ODriveCommand_Response msg_;
};

class Init_ODriveCommand_Response_success
{
public:
  Init_ODriveCommand_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ODriveCommand_Response_message success(::custom_msgs::srv::ODriveCommand_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_ODriveCommand_Response_message(msg_);
  }

private:
  ::custom_msgs::srv::ODriveCommand_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::srv::ODriveCommand_Response>()
{
  return custom_msgs::srv::builder::Init_ODriveCommand_Response_success();
}

}  // namespace custom_msgs

#endif  // CUSTOM_MSGS__SRV__DETAIL__O_DRIVE_COMMAND__BUILDER_HPP_
