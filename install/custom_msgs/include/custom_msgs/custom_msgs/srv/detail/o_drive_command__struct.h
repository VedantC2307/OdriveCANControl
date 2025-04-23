// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_msgs:srv/ODriveCommand.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__SRV__DETAIL__O_DRIVE_COMMAND__STRUCT_H_
#define CUSTOM_MSGS__SRV__DETAIL__O_DRIVE_COMMAND__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'command'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/ODriveCommand in the package custom_msgs.
typedef struct custom_msgs__srv__ODriveCommand_Request
{
  /// initialize, clear_error, set_idle, set_closed_loop
  rosidl_runtime_c__String command;
} custom_msgs__srv__ODriveCommand_Request;

// Struct for a sequence of custom_msgs__srv__ODriveCommand_Request.
typedef struct custom_msgs__srv__ODriveCommand_Request__Sequence
{
  custom_msgs__srv__ODriveCommand_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_msgs__srv__ODriveCommand_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/ODriveCommand in the package custom_msgs.
typedef struct custom_msgs__srv__ODriveCommand_Response
{
  /// check sucess
  bool success;
  /// results message
  rosidl_runtime_c__String message;
} custom_msgs__srv__ODriveCommand_Response;

// Struct for a sequence of custom_msgs__srv__ODriveCommand_Response.
typedef struct custom_msgs__srv__ODriveCommand_Response__Sequence
{
  custom_msgs__srv__ODriveCommand_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_msgs__srv__ODriveCommand_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_MSGS__SRV__DETAIL__O_DRIVE_COMMAND__STRUCT_H_
