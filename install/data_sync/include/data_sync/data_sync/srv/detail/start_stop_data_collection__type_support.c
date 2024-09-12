// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from data_sync:srv/StartStopDataCollection.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "data_sync/srv/detail/start_stop_data_collection__rosidl_typesupport_introspection_c.h"
#include "data_sync/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "data_sync/srv/detail/start_stop_data_collection__functions.h"
#include "data_sync/srv/detail/start_stop_data_collection__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void data_sync__srv__StartStopDataCollection_Request__rosidl_typesupport_introspection_c__StartStopDataCollection_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  data_sync__srv__StartStopDataCollection_Request__init(message_memory);
}

void data_sync__srv__StartStopDataCollection_Request__rosidl_typesupport_introspection_c__StartStopDataCollection_Request_fini_function(void * message_memory)
{
  data_sync__srv__StartStopDataCollection_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember data_sync__srv__StartStopDataCollection_Request__rosidl_typesupport_introspection_c__StartStopDataCollection_Request_message_member_array[1] = {
  {
    "start",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(data_sync__srv__StartStopDataCollection_Request, start),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers data_sync__srv__StartStopDataCollection_Request__rosidl_typesupport_introspection_c__StartStopDataCollection_Request_message_members = {
  "data_sync__srv",  // message namespace
  "StartStopDataCollection_Request",  // message name
  1,  // number of fields
  sizeof(data_sync__srv__StartStopDataCollection_Request),
  data_sync__srv__StartStopDataCollection_Request__rosidl_typesupport_introspection_c__StartStopDataCollection_Request_message_member_array,  // message members
  data_sync__srv__StartStopDataCollection_Request__rosidl_typesupport_introspection_c__StartStopDataCollection_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  data_sync__srv__StartStopDataCollection_Request__rosidl_typesupport_introspection_c__StartStopDataCollection_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t data_sync__srv__StartStopDataCollection_Request__rosidl_typesupport_introspection_c__StartStopDataCollection_Request_message_type_support_handle = {
  0,
  &data_sync__srv__StartStopDataCollection_Request__rosidl_typesupport_introspection_c__StartStopDataCollection_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_data_sync
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, data_sync, srv, StartStopDataCollection_Request)() {
  if (!data_sync__srv__StartStopDataCollection_Request__rosidl_typesupport_introspection_c__StartStopDataCollection_Request_message_type_support_handle.typesupport_identifier) {
    data_sync__srv__StartStopDataCollection_Request__rosidl_typesupport_introspection_c__StartStopDataCollection_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &data_sync__srv__StartStopDataCollection_Request__rosidl_typesupport_introspection_c__StartStopDataCollection_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "data_sync/srv/detail/start_stop_data_collection__rosidl_typesupport_introspection_c.h"
// already included above
// #include "data_sync/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "data_sync/srv/detail/start_stop_data_collection__functions.h"
// already included above
// #include "data_sync/srv/detail/start_stop_data_collection__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void data_sync__srv__StartStopDataCollection_Response__rosidl_typesupport_introspection_c__StartStopDataCollection_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  data_sync__srv__StartStopDataCollection_Response__init(message_memory);
}

void data_sync__srv__StartStopDataCollection_Response__rosidl_typesupport_introspection_c__StartStopDataCollection_Response_fini_function(void * message_memory)
{
  data_sync__srv__StartStopDataCollection_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember data_sync__srv__StartStopDataCollection_Response__rosidl_typesupport_introspection_c__StartStopDataCollection_Response_message_member_array[1] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(data_sync__srv__StartStopDataCollection_Response, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers data_sync__srv__StartStopDataCollection_Response__rosidl_typesupport_introspection_c__StartStopDataCollection_Response_message_members = {
  "data_sync__srv",  // message namespace
  "StartStopDataCollection_Response",  // message name
  1,  // number of fields
  sizeof(data_sync__srv__StartStopDataCollection_Response),
  data_sync__srv__StartStopDataCollection_Response__rosidl_typesupport_introspection_c__StartStopDataCollection_Response_message_member_array,  // message members
  data_sync__srv__StartStopDataCollection_Response__rosidl_typesupport_introspection_c__StartStopDataCollection_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  data_sync__srv__StartStopDataCollection_Response__rosidl_typesupport_introspection_c__StartStopDataCollection_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t data_sync__srv__StartStopDataCollection_Response__rosidl_typesupport_introspection_c__StartStopDataCollection_Response_message_type_support_handle = {
  0,
  &data_sync__srv__StartStopDataCollection_Response__rosidl_typesupport_introspection_c__StartStopDataCollection_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_data_sync
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, data_sync, srv, StartStopDataCollection_Response)() {
  if (!data_sync__srv__StartStopDataCollection_Response__rosidl_typesupport_introspection_c__StartStopDataCollection_Response_message_type_support_handle.typesupport_identifier) {
    data_sync__srv__StartStopDataCollection_Response__rosidl_typesupport_introspection_c__StartStopDataCollection_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &data_sync__srv__StartStopDataCollection_Response__rosidl_typesupport_introspection_c__StartStopDataCollection_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "data_sync/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "data_sync/srv/detail/start_stop_data_collection__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers data_sync__srv__detail__start_stop_data_collection__rosidl_typesupport_introspection_c__StartStopDataCollection_service_members = {
  "data_sync__srv",  // service namespace
  "StartStopDataCollection",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // data_sync__srv__detail__start_stop_data_collection__rosidl_typesupport_introspection_c__StartStopDataCollection_Request_message_type_support_handle,
  NULL  // response message
  // data_sync__srv__detail__start_stop_data_collection__rosidl_typesupport_introspection_c__StartStopDataCollection_Response_message_type_support_handle
};

static rosidl_service_type_support_t data_sync__srv__detail__start_stop_data_collection__rosidl_typesupport_introspection_c__StartStopDataCollection_service_type_support_handle = {
  0,
  &data_sync__srv__detail__start_stop_data_collection__rosidl_typesupport_introspection_c__StartStopDataCollection_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, data_sync, srv, StartStopDataCollection_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, data_sync, srv, StartStopDataCollection_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_data_sync
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, data_sync, srv, StartStopDataCollection)() {
  if (!data_sync__srv__detail__start_stop_data_collection__rosidl_typesupport_introspection_c__StartStopDataCollection_service_type_support_handle.typesupport_identifier) {
    data_sync__srv__detail__start_stop_data_collection__rosidl_typesupport_introspection_c__StartStopDataCollection_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)data_sync__srv__detail__start_stop_data_collection__rosidl_typesupport_introspection_c__StartStopDataCollection_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, data_sync, srv, StartStopDataCollection_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, data_sync, srv, StartStopDataCollection_Response)()->data;
  }

  return &data_sync__srv__detail__start_stop_data_collection__rosidl_typesupport_introspection_c__StartStopDataCollection_service_type_support_handle;
}
