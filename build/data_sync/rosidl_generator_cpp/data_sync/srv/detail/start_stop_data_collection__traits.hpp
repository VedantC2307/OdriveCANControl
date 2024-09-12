// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from data_sync:srv/StartStopDataCollection.idl
// generated code does not contain a copyright notice

#ifndef DATA_SYNC__SRV__DETAIL__START_STOP_DATA_COLLECTION__TRAITS_HPP_
#define DATA_SYNC__SRV__DETAIL__START_STOP_DATA_COLLECTION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "data_sync/srv/detail/start_stop_data_collection__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace data_sync
{

namespace srv
{

inline void to_flow_style_yaml(
  const StartStopDataCollection_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: start
  {
    out << "start: ";
    rosidl_generator_traits::value_to_yaml(msg.start, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const StartStopDataCollection_Request & msg,
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
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const StartStopDataCollection_Request & msg, bool use_flow_style = false)
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
  const data_sync::srv::StartStopDataCollection_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  data_sync::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use data_sync::srv::to_yaml() instead")]]
inline std::string to_yaml(const data_sync::srv::StartStopDataCollection_Request & msg)
{
  return data_sync::srv::to_yaml(msg);
}

template<>
inline const char * data_type<data_sync::srv::StartStopDataCollection_Request>()
{
  return "data_sync::srv::StartStopDataCollection_Request";
}

template<>
inline const char * name<data_sync::srv::StartStopDataCollection_Request>()
{
  return "data_sync/srv/StartStopDataCollection_Request";
}

template<>
struct has_fixed_size<data_sync::srv::StartStopDataCollection_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<data_sync::srv::StartStopDataCollection_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<data_sync::srv::StartStopDataCollection_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace data_sync
{

namespace srv
{

inline void to_flow_style_yaml(
  const StartStopDataCollection_Response & msg,
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
  const StartStopDataCollection_Response & msg,
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

inline std::string to_yaml(const StartStopDataCollection_Response & msg, bool use_flow_style = false)
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
  const data_sync::srv::StartStopDataCollection_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  data_sync::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use data_sync::srv::to_yaml() instead")]]
inline std::string to_yaml(const data_sync::srv::StartStopDataCollection_Response & msg)
{
  return data_sync::srv::to_yaml(msg);
}

template<>
inline const char * data_type<data_sync::srv::StartStopDataCollection_Response>()
{
  return "data_sync::srv::StartStopDataCollection_Response";
}

template<>
inline const char * name<data_sync::srv::StartStopDataCollection_Response>()
{
  return "data_sync/srv/StartStopDataCollection_Response";
}

template<>
struct has_fixed_size<data_sync::srv::StartStopDataCollection_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<data_sync::srv::StartStopDataCollection_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<data_sync::srv::StartStopDataCollection_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<data_sync::srv::StartStopDataCollection>()
{
  return "data_sync::srv::StartStopDataCollection";
}

template<>
inline const char * name<data_sync::srv::StartStopDataCollection>()
{
  return "data_sync/srv/StartStopDataCollection";
}

template<>
struct has_fixed_size<data_sync::srv::StartStopDataCollection>
  : std::integral_constant<
    bool,
    has_fixed_size<data_sync::srv::StartStopDataCollection_Request>::value &&
    has_fixed_size<data_sync::srv::StartStopDataCollection_Response>::value
  >
{
};

template<>
struct has_bounded_size<data_sync::srv::StartStopDataCollection>
  : std::integral_constant<
    bool,
    has_bounded_size<data_sync::srv::StartStopDataCollection_Request>::value &&
    has_bounded_size<data_sync::srv::StartStopDataCollection_Response>::value
  >
{
};

template<>
struct is_service<data_sync::srv::StartStopDataCollection>
  : std::true_type
{
};

template<>
struct is_service_request<data_sync::srv::StartStopDataCollection_Request>
  : std::true_type
{
};

template<>
struct is_service_response<data_sync::srv::StartStopDataCollection_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // DATA_SYNC__SRV__DETAIL__START_STOP_DATA_COLLECTION__TRAITS_HPP_
