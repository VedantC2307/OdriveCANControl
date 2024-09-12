// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from data_sync:srv/Trigger.idl
// generated code does not contain a copyright notice

#ifndef DATA_SYNC__SRV__DETAIL__TRIGGER__BUILDER_HPP_
#define DATA_SYNC__SRV__DETAIL__TRIGGER__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "data_sync/srv/detail/trigger__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace data_sync
{

namespace srv
{

namespace builder
{

class Init_Trigger_Request_filename
{
public:
  explicit Init_Trigger_Request_filename(::data_sync::srv::Trigger_Request & msg)
  : msg_(msg)
  {}
  ::data_sync::srv::Trigger_Request filename(::data_sync::srv::Trigger_Request::_filename_type arg)
  {
    msg_.filename = std::move(arg);
    return std::move(msg_);
  }

private:
  ::data_sync::srv::Trigger_Request msg_;
};

class Init_Trigger_Request_topic_name_2
{
public:
  explicit Init_Trigger_Request_topic_name_2(::data_sync::srv::Trigger_Request & msg)
  : msg_(msg)
  {}
  Init_Trigger_Request_filename topic_name_2(::data_sync::srv::Trigger_Request::_topic_name_2_type arg)
  {
    msg_.topic_name_2 = std::move(arg);
    return Init_Trigger_Request_filename(msg_);
  }

private:
  ::data_sync::srv::Trigger_Request msg_;
};

class Init_Trigger_Request_topic_name_1
{
public:
  explicit Init_Trigger_Request_topic_name_1(::data_sync::srv::Trigger_Request & msg)
  : msg_(msg)
  {}
  Init_Trigger_Request_topic_name_2 topic_name_1(::data_sync::srv::Trigger_Request::_topic_name_1_type arg)
  {
    msg_.topic_name_1 = std::move(arg);
    return Init_Trigger_Request_topic_name_2(msg_);
  }

private:
  ::data_sync::srv::Trigger_Request msg_;
};

class Init_Trigger_Request_start
{
public:
  Init_Trigger_Request_start()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Trigger_Request_topic_name_1 start(::data_sync::srv::Trigger_Request::_start_type arg)
  {
    msg_.start = std::move(arg);
    return Init_Trigger_Request_topic_name_1(msg_);
  }

private:
  ::data_sync::srv::Trigger_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::data_sync::srv::Trigger_Request>()
{
  return data_sync::srv::builder::Init_Trigger_Request_start();
}

}  // namespace data_sync


namespace data_sync
{

namespace srv
{

namespace builder
{

class Init_Trigger_Response_success
{
public:
  Init_Trigger_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::data_sync::srv::Trigger_Response success(::data_sync::srv::Trigger_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::data_sync::srv::Trigger_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::data_sync::srv::Trigger_Response>()
{
  return data_sync::srv::builder::Init_Trigger_Response_success();
}

}  // namespace data_sync

#endif  // DATA_SYNC__SRV__DETAIL__TRIGGER__BUILDER_HPP_
