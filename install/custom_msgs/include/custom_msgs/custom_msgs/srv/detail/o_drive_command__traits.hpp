// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from custom_msgs:srv/ODriveCommand.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__SRV__DETAIL__O_DRIVE_COMMAND__TRAITS_HPP_
#define CUSTOM_MSGS__SRV__DETAIL__O_DRIVE_COMMAND__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "custom_msgs/srv/detail/o_drive_command__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace custom_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const ODriveCommand_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: command
  {
    out << "command: ";
    rosidl_generator_traits::value_to_yaml(msg.command, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ODriveCommand_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: command
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "command: ";
    rosidl_generator_traits::value_to_yaml(msg.command, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ODriveCommand_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace custom_msgs

namespace rosidl_generator_traits
{

[[deprecated("use custom_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msgs::srv::ODriveCommand_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const custom_msgs::srv::ODriveCommand_Request & msg)
{
  return custom_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msgs::srv::ODriveCommand_Request>()
{
  return "custom_msgs::srv::ODriveCommand_Request";
}

template<>
inline const char * name<custom_msgs::srv::ODriveCommand_Request>()
{
  return "custom_msgs/srv/ODriveCommand_Request";
}

template<>
struct has_fixed_size<custom_msgs::srv::ODriveCommand_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<custom_msgs::srv::ODriveCommand_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<custom_msgs::srv::ODriveCommand_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace custom_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const ODriveCommand_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ODriveCommand_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ODriveCommand_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace custom_msgs

namespace rosidl_generator_traits
{

[[deprecated("use custom_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msgs::srv::ODriveCommand_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const custom_msgs::srv::ODriveCommand_Response & msg)
{
  return custom_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msgs::srv::ODriveCommand_Response>()
{
  return "custom_msgs::srv::ODriveCommand_Response";
}

template<>
inline const char * name<custom_msgs::srv::ODriveCommand_Response>()
{
  return "custom_msgs/srv/ODriveCommand_Response";
}

template<>
struct has_fixed_size<custom_msgs::srv::ODriveCommand_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<custom_msgs::srv::ODriveCommand_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<custom_msgs::srv::ODriveCommand_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<custom_msgs::srv::ODriveCommand>()
{
  return "custom_msgs::srv::ODriveCommand";
}

template<>
inline const char * name<custom_msgs::srv::ODriveCommand>()
{
  return "custom_msgs/srv/ODriveCommand";
}

template<>
struct has_fixed_size<custom_msgs::srv::ODriveCommand>
  : std::integral_constant<
    bool,
    has_fixed_size<custom_msgs::srv::ODriveCommand_Request>::value &&
    has_fixed_size<custom_msgs::srv::ODriveCommand_Response>::value
  >
{
};

template<>
struct has_bounded_size<custom_msgs::srv::ODriveCommand>
  : std::integral_constant<
    bool,
    has_bounded_size<custom_msgs::srv::ODriveCommand_Request>::value &&
    has_bounded_size<custom_msgs::srv::ODriveCommand_Response>::value
  >
{
};

template<>
struct is_service<custom_msgs::srv::ODriveCommand>
  : std::true_type
{
};

template<>
struct is_service_request<custom_msgs::srv::ODriveCommand_Request>
  : std::true_type
{
};

template<>
struct is_service_response<custom_msgs::srv::ODriveCommand_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // CUSTOM_MSGS__SRV__DETAIL__O_DRIVE_COMMAND__TRAITS_HPP_
