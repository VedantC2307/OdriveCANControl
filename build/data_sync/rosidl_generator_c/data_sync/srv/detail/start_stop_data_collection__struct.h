// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from data_sync:srv/StartStopDataCollection.idl
// generated code does not contain a copyright notice

#ifndef DATA_SYNC__SRV__DETAIL__START_STOP_DATA_COLLECTION__STRUCT_H_
#define DATA_SYNC__SRV__DETAIL__START_STOP_DATA_COLLECTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/StartStopDataCollection in the package data_sync.
typedef struct data_sync__srv__StartStopDataCollection_Request
{
  bool start;
} data_sync__srv__StartStopDataCollection_Request;

// Struct for a sequence of data_sync__srv__StartStopDataCollection_Request.
typedef struct data_sync__srv__StartStopDataCollection_Request__Sequence
{
  data_sync__srv__StartStopDataCollection_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} data_sync__srv__StartStopDataCollection_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/StartStopDataCollection in the package data_sync.
typedef struct data_sync__srv__StartStopDataCollection_Response
{
  bool success;
} data_sync__srv__StartStopDataCollection_Response;

// Struct for a sequence of data_sync__srv__StartStopDataCollection_Response.
typedef struct data_sync__srv__StartStopDataCollection_Response__Sequence
{
  data_sync__srv__StartStopDataCollection_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} data_sync__srv__StartStopDataCollection_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DATA_SYNC__SRV__DETAIL__START_STOP_DATA_COLLECTION__STRUCT_H_
