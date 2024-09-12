// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from data_sync:srv/StartStopDataCollection.idl
// generated code does not contain a copyright notice

#ifndef DATA_SYNC__SRV__DETAIL__START_STOP_DATA_COLLECTION__STRUCT_HPP_
#define DATA_SYNC__SRV__DETAIL__START_STOP_DATA_COLLECTION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__data_sync__srv__StartStopDataCollection_Request __attribute__((deprecated))
#else
# define DEPRECATED__data_sync__srv__StartStopDataCollection_Request __declspec(deprecated)
#endif

namespace data_sync
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct StartStopDataCollection_Request_
{
  using Type = StartStopDataCollection_Request_<ContainerAllocator>;

  explicit StartStopDataCollection_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->start = false;
    }
  }

  explicit StartStopDataCollection_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->start = false;
    }
  }

  // field types and members
  using _start_type =
    bool;
  _start_type start;

  // setters for named parameter idiom
  Type & set__start(
    const bool & _arg)
  {
    this->start = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    data_sync::srv::StartStopDataCollection_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const data_sync::srv::StartStopDataCollection_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<data_sync::srv::StartStopDataCollection_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<data_sync::srv::StartStopDataCollection_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      data_sync::srv::StartStopDataCollection_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<data_sync::srv::StartStopDataCollection_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      data_sync::srv::StartStopDataCollection_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<data_sync::srv::StartStopDataCollection_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<data_sync::srv::StartStopDataCollection_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<data_sync::srv::StartStopDataCollection_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__data_sync__srv__StartStopDataCollection_Request
    std::shared_ptr<data_sync::srv::StartStopDataCollection_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__data_sync__srv__StartStopDataCollection_Request
    std::shared_ptr<data_sync::srv::StartStopDataCollection_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const StartStopDataCollection_Request_ & other) const
  {
    if (this->start != other.start) {
      return false;
    }
    return true;
  }
  bool operator!=(const StartStopDataCollection_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct StartStopDataCollection_Request_

// alias to use template instance with default allocator
using StartStopDataCollection_Request =
  data_sync::srv::StartStopDataCollection_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace data_sync


#ifndef _WIN32
# define DEPRECATED__data_sync__srv__StartStopDataCollection_Response __attribute__((deprecated))
#else
# define DEPRECATED__data_sync__srv__StartStopDataCollection_Response __declspec(deprecated)
#endif

namespace data_sync
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct StartStopDataCollection_Response_
{
  using Type = StartStopDataCollection_Response_<ContainerAllocator>;

  explicit StartStopDataCollection_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
    }
  }

  explicit StartStopDataCollection_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    data_sync::srv::StartStopDataCollection_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const data_sync::srv::StartStopDataCollection_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<data_sync::srv::StartStopDataCollection_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<data_sync::srv::StartStopDataCollection_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      data_sync::srv::StartStopDataCollection_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<data_sync::srv::StartStopDataCollection_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      data_sync::srv::StartStopDataCollection_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<data_sync::srv::StartStopDataCollection_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<data_sync::srv::StartStopDataCollection_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<data_sync::srv::StartStopDataCollection_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__data_sync__srv__StartStopDataCollection_Response
    std::shared_ptr<data_sync::srv::StartStopDataCollection_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__data_sync__srv__StartStopDataCollection_Response
    std::shared_ptr<data_sync::srv::StartStopDataCollection_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const StartStopDataCollection_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    return true;
  }
  bool operator!=(const StartStopDataCollection_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct StartStopDataCollection_Response_

// alias to use template instance with default allocator
using StartStopDataCollection_Response =
  data_sync::srv::StartStopDataCollection_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace data_sync

namespace data_sync
{

namespace srv
{

struct StartStopDataCollection
{
  using Request = data_sync::srv::StartStopDataCollection_Request;
  using Response = data_sync::srv::StartStopDataCollection_Response;
};

}  // namespace srv

}  // namespace data_sync

#endif  // DATA_SYNC__SRV__DETAIL__START_STOP_DATA_COLLECTION__STRUCT_HPP_
