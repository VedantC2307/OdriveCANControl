// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from data_sync:srv/StartStopDataCollection.idl
// generated code does not contain a copyright notice

#ifndef DATA_SYNC__SRV__DETAIL__START_STOP_DATA_COLLECTION__BUILDER_HPP_
#define DATA_SYNC__SRV__DETAIL__START_STOP_DATA_COLLECTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "data_sync/srv/detail/start_stop_data_collection__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace data_sync
{

namespace srv
{

namespace builder
{

class Init_StartStopDataCollection_Request_start
{
public:
  Init_StartStopDataCollection_Request_start()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::data_sync::srv::StartStopDataCollection_Request start(::data_sync::srv::StartStopDataCollection_Request::_start_type arg)
  {
    msg_.start = std::move(arg);
    return std::move(msg_);
  }

private:
  ::data_sync::srv::StartStopDataCollection_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::data_sync::srv::StartStopDataCollection_Request>()
{
  return data_sync::srv::builder::Init_StartStopDataCollection_Request_start();
}

}  // namespace data_sync


namespace data_sync
{

namespace srv
{

namespace builder
{

class Init_StartStopDataCollection_Response_success
{
public:
  Init_StartStopDataCollection_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::data_sync::srv::StartStopDataCollection_Response success(::data_sync::srv::StartStopDataCollection_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::data_sync::srv::StartStopDataCollection_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::data_sync::srv::StartStopDataCollection_Response>()
{
  return data_sync::srv::builder::Init_StartStopDataCollection_Response_success();
}

}  // namespace data_sync

#endif  // DATA_SYNC__SRV__DETAIL__START_STOP_DATA_COLLECTION__BUILDER_HPP_
