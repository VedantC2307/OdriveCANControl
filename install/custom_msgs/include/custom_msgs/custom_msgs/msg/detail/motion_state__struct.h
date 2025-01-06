// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_msgs:msg/MotionState.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__MSG__DETAIL__MOTION_STATE__STRUCT_H_
#define CUSTOM_MSGS__MSG__DETAIL__MOTION_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/MotionState in the package custom_msgs.
typedef struct custom_msgs__msg__MotionState
{
  float position;
  float velocity;
} custom_msgs__msg__MotionState;

// Struct for a sequence of custom_msgs__msg__MotionState.
typedef struct custom_msgs__msg__MotionState__Sequence
{
  custom_msgs__msg__MotionState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_msgs__msg__MotionState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_MSGS__MSG__DETAIL__MOTION_STATE__STRUCT_H_
