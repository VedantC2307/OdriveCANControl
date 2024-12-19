// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from data_sync:srv/Trigger.idl
// generated code does not contain a copyright notice

#ifndef DATA_SYNC__SRV__DETAIL__TRIGGER__STRUCT_H_
#define DATA_SYNC__SRV__DETAIL__TRIGGER__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'topic_name_1'
// Member 'topic_name_2'
// Member 'filename'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/Trigger in the package data_sync.
typedef struct data_sync__srv__Trigger_Request
{
  bool start;
  rosidl_runtime_c__String topic_name_1;
  rosidl_runtime_c__String topic_name_2;
  rosidl_runtime_c__String filename;
} data_sync__srv__Trigger_Request;

// Struct for a sequence of data_sync__srv__Trigger_Request.
typedef struct data_sync__srv__Trigger_Request__Sequence
{
  data_sync__srv__Trigger_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} data_sync__srv__Trigger_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/Trigger in the package data_sync.
typedef struct data_sync__srv__Trigger_Response
{
  bool success;
} data_sync__srv__Trigger_Response;

// Struct for a sequence of data_sync__srv__Trigger_Response.
typedef struct data_sync__srv__Trigger_Response__Sequence
{
  data_sync__srv__Trigger_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} data_sync__srv__Trigger_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DATA_SYNC__SRV__DETAIL__TRIGGER__STRUCT_H_
