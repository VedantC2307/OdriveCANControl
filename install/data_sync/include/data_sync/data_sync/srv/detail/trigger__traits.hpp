// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from data_sync:srv/Trigger.idl
// generated code does not contain a copyright notice

#ifndef DATA_SYNC__SRV__DETAIL__TRIGGER__TRAITS_HPP_
#define DATA_SYNC__SRV__DETAIL__TRIGGER__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "data_sync/srv/detail/trigger__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace data_sync
{

namespace srv
{

inline void to_flow_style_yaml(
  const Trigger_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: start
  {
    out << "start: ";
    rosidl_generator_traits::value_to_yaml(msg.start, out);
    out << ", ";
  }

  // member: topic_name_1
  {
    out << "topic_name_1: ";
    rosidl_generator_traits::value_to_yaml(msg.topic_name_1, out);
    out << ", ";
  }

  // member: topic_name_2
  {
    out << "topic_name_2: ";
    rosidl_generator_traits::value_to_yaml(msg.topic_name_2, out);
    out << ", ";
  }

  // member: filename
  {
    out << "filename: ";
    rosidl_generator_traits::value_to_yaml(msg.filename, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Trigger_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: start
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "start: ";
    rosidl_generator_traits::value_to_yaml(msg.start, out);
    out << "\n";
  }

  // member: topic_name_1
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "topic_name_1: ";
    rosidl_generator_traits::value_to_yaml(msg.topic_name_1, out);
    out << "\n";
  }

  // member: topic_name_2
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "topic_name_2: ";
    rosidl_generator_traits::value_to_yaml(msg.topic_name_2, out);
    out << "\n";
  }

  // member: filename
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "filename: ";
    rosidl_generator_traits::value_to_yaml(msg.filename, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Trigger_Request & msg, bool use_flow_style = false)
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

}  // namespace data_sync

namespace rosidl_generator_traits
{

[[deprecated("use data_sync::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const data_sync::srv::Trigger_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  data_sync::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use data_sync::srv::to_yaml() instead")]]
inline std::string to_yaml(const data_sync::srv::Trigger_Request & msg)
{
  return data_sync::srv::to_yaml(msg);
}

template<>
inline const char * data_type<data_sync::srv::Trigger_Request>()
{
  return "data_sync::srv::Trigger_Request";
}

template<>
inline const char * name<data_sync::srv::Trigger_Request>()
{
  return "data_sync/srv/Trigger_Request";
}

template<>
struct has_fixed_size<data_sync::srv::Trigger_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<data_sync::srv::Trigger_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<data_sync::srv::Trigger_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace data_sync
{

namespace srv
{

inline void to_flow_style_yaml(
  const Trigger_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Trigger_Response & msg,
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
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Trigger_Response & msg, bool use_flow_style = false)
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

}  // namespace data_sync

namespace rosidl_generator_traits
{

[[deprecated("use data_sync::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const data_sync::srv::Trigger_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  data_sync::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use data_sync::srv::to_yaml() instead")]]
inline std::string to_yaml(const data_sync::srv::Trigger_Response & msg)
{
  return data_sync::srv::to_yaml(msg);
}

template<>
inline const char * data_type<data_sync::srv::Trigger_Response>()
{
  return "data_sync::srv::Trigger_Response";
}

template<>
inline const char * name<data_sync::srv::Trigger_Response>()
{
  return "data_sync/srv/Trigger_Response";
}

template<>
struct has_fixed_size<data_sync::srv::Trigger_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<data_sync::srv::Trigger_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<data_sync::srv::Trigger_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<data_sync::srv::Trigger>()
{
  return "data_sync::srv::Trigger";
}

template<>
inline const char * name<data_sync::srv::Trigger>()
{
  return "data_sync/srv/Trigger";
}

template<>
struct has_fixed_size<data_sync::srv::Trigger>
  : std::integral_constant<
    bool,
    has_fixed_size<data_sync::srv::Trigger_Request>::value &&
    has_fixed_size<data_sync::srv::Trigger_Response>::value
  >
{
};

template<>
struct has_bounded_size<data_sync::srv::Trigger>
  : std::integral_constant<
    bool,
    has_bounded_size<data_sync::srv::Trigger_Request>::value &&
    has_bounded_size<data_sync::srv::Trigger_Response>::value
  >
{
};

template<>
struct is_service<data_sync::srv::Trigger>
  : std::true_type
{
};

template<>
struct is_service_request<data_sync::srv::Trigger_Request>
  : std::true_type
{
};

template<>
struct is_service_response<data_sync::srv::Trigger_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // DATA_SYNC__SRV__DETAIL__TRIGGER__TRAITS_HPP_
