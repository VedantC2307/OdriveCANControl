// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_msgs:msg/FrictionComp.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__MSG__DETAIL__FRICTION_COMP__STRUCT_HPP_
#define CUSTOM_MSGS__MSG__DETAIL__FRICTION_COMP__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__custom_msgs__msg__FrictionComp __attribute__((deprecated))
#else
# define DEPRECATED__custom_msgs__msg__FrictionComp __declspec(deprecated)
#endif

namespace custom_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct FrictionComp_
{
  using Type = FrictionComp_<ContainerAllocator>;

  explicit FrictionComp_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->tau_fcomp = 0.0f;
    }
  }

  explicit FrictionComp_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->tau_fcomp = 0.0f;
    }
  }

  // field types and members
  using _tau_fcomp_type =
    float;
  _tau_fcomp_type tau_fcomp;

  // setters for named parameter idiom
  Type & set__tau_fcomp(
    const float & _arg)
  {
    this->tau_fcomp = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_msgs::msg::FrictionComp_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_msgs::msg::FrictionComp_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_msgs::msg::FrictionComp_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_msgs::msg::FrictionComp_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_msgs::msg::FrictionComp_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_msgs::msg::FrictionComp_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_msgs::msg::FrictionComp_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_msgs::msg::FrictionComp_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_msgs::msg::FrictionComp_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_msgs::msg::FrictionComp_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_msgs__msg__FrictionComp
    std::shared_ptr<custom_msgs::msg::FrictionComp_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_msgs__msg__FrictionComp
    std::shared_ptr<custom_msgs::msg::FrictionComp_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const FrictionComp_ & other) const
  {
    if (this->tau_fcomp != other.tau_fcomp) {
      return false;
    }
    return true;
  }
  bool operator!=(const FrictionComp_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct FrictionComp_

// alias to use template instance with default allocator
using FrictionComp =
  custom_msgs::msg::FrictionComp_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace custom_msgs

#endif  // CUSTOM_MSGS__MSG__DETAIL__FRICTION_COMP__STRUCT_HPP_
