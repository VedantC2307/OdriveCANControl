// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from data_sync:srv/Trigger.idl
// generated code does not contain a copyright notice
#include "data_sync/srv/detail/trigger__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `topic_name_1`
// Member `topic_name_2`
// Member `filename`
#include "rosidl_runtime_c/string_functions.h"

bool
data_sync__srv__Trigger_Request__init(data_sync__srv__Trigger_Request * msg)
{
  if (!msg) {
    return false;
  }
  // start
  // topic_name_1
  if (!rosidl_runtime_c__String__init(&msg->topic_name_1)) {
    data_sync__srv__Trigger_Request__fini(msg);
    return false;
  }
  // topic_name_2
  if (!rosidl_runtime_c__String__init(&msg->topic_name_2)) {
    data_sync__srv__Trigger_Request__fini(msg);
    return false;
  }
  // filename
  if (!rosidl_runtime_c__String__init(&msg->filename)) {
    data_sync__srv__Trigger_Request__fini(msg);
    return false;
  }
  return true;
}

void
data_sync__srv__Trigger_Request__fini(data_sync__srv__Trigger_Request * msg)
{
  if (!msg) {
    return;
  }
  // start
  // topic_name_1
  rosidl_runtime_c__String__fini(&msg->topic_name_1);
  // topic_name_2
  rosidl_runtime_c__String__fini(&msg->topic_name_2);
  // filename
  rosidl_runtime_c__String__fini(&msg->filename);
}

bool
data_sync__srv__Trigger_Request__are_equal(const data_sync__srv__Trigger_Request * lhs, const data_sync__srv__Trigger_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // start
  if (lhs->start != rhs->start) {
    return false;
  }
  // topic_name_1
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->topic_name_1), &(rhs->topic_name_1)))
  {
    return false;
  }
  // topic_name_2
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->topic_name_2), &(rhs->topic_name_2)))
  {
    return false;
  }
  // filename
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->filename), &(rhs->filename)))
  {
    return false;
  }
  return true;
}

bool
data_sync__srv__Trigger_Request__copy(
  const data_sync__srv__Trigger_Request * input,
  data_sync__srv__Trigger_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // start
  output->start = input->start;
  // topic_name_1
  if (!rosidl_runtime_c__String__copy(
      &(input->topic_name_1), &(output->topic_name_1)))
  {
    return false;
  }
  // topic_name_2
  if (!rosidl_runtime_c__String__copy(
      &(input->topic_name_2), &(output->topic_name_2)))
  {
    return false;
  }
  // filename
  if (!rosidl_runtime_c__String__copy(
      &(input->filename), &(output->filename)))
  {
    return false;
  }
  return true;
}

data_sync__srv__Trigger_Request *
data_sync__srv__Trigger_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  data_sync__srv__Trigger_Request * msg = (data_sync__srv__Trigger_Request *)allocator.allocate(sizeof(data_sync__srv__Trigger_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(data_sync__srv__Trigger_Request));
  bool success = data_sync__srv__Trigger_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
data_sync__srv__Trigger_Request__destroy(data_sync__srv__Trigger_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    data_sync__srv__Trigger_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
data_sync__srv__Trigger_Request__Sequence__init(data_sync__srv__Trigger_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  data_sync__srv__Trigger_Request * data = NULL;

  if (size) {
    data = (data_sync__srv__Trigger_Request *)allocator.zero_allocate(size, sizeof(data_sync__srv__Trigger_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = data_sync__srv__Trigger_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        data_sync__srv__Trigger_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
data_sync__srv__Trigger_Request__Sequence__fini(data_sync__srv__Trigger_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      data_sync__srv__Trigger_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

data_sync__srv__Trigger_Request__Sequence *
data_sync__srv__Trigger_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  data_sync__srv__Trigger_Request__Sequence * array = (data_sync__srv__Trigger_Request__Sequence *)allocator.allocate(sizeof(data_sync__srv__Trigger_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = data_sync__srv__Trigger_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
data_sync__srv__Trigger_Request__Sequence__destroy(data_sync__srv__Trigger_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    data_sync__srv__Trigger_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
data_sync__srv__Trigger_Request__Sequence__are_equal(const data_sync__srv__Trigger_Request__Sequence * lhs, const data_sync__srv__Trigger_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!data_sync__srv__Trigger_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
data_sync__srv__Trigger_Request__Sequence__copy(
  const data_sync__srv__Trigger_Request__Sequence * input,
  data_sync__srv__Trigger_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(data_sync__srv__Trigger_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    data_sync__srv__Trigger_Request * data =
      (data_sync__srv__Trigger_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!data_sync__srv__Trigger_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          data_sync__srv__Trigger_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!data_sync__srv__Trigger_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


bool
data_sync__srv__Trigger_Response__init(data_sync__srv__Trigger_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  return true;
}

void
data_sync__srv__Trigger_Response__fini(data_sync__srv__Trigger_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
}

bool
data_sync__srv__Trigger_Response__are_equal(const data_sync__srv__Trigger_Response * lhs, const data_sync__srv__Trigger_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  return true;
}

bool
data_sync__srv__Trigger_Response__copy(
  const data_sync__srv__Trigger_Response * input,
  data_sync__srv__Trigger_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  return true;
}

data_sync__srv__Trigger_Response *
data_sync__srv__Trigger_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  data_sync__srv__Trigger_Response * msg = (data_sync__srv__Trigger_Response *)allocator.allocate(sizeof(data_sync__srv__Trigger_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(data_sync__srv__Trigger_Response));
  bool success = data_sync__srv__Trigger_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
data_sync__srv__Trigger_Response__destroy(data_sync__srv__Trigger_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    data_sync__srv__Trigger_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
data_sync__srv__Trigger_Response__Sequence__init(data_sync__srv__Trigger_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  data_sync__srv__Trigger_Response * data = NULL;

  if (size) {
    data = (data_sync__srv__Trigger_Response *)allocator.zero_allocate(size, sizeof(data_sync__srv__Trigger_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = data_sync__srv__Trigger_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        data_sync__srv__Trigger_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
data_sync__srv__Trigger_Response__Sequence__fini(data_sync__srv__Trigger_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      data_sync__srv__Trigger_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

data_sync__srv__Trigger_Response__Sequence *
data_sync__srv__Trigger_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  data_sync__srv__Trigger_Response__Sequence * array = (data_sync__srv__Trigger_Response__Sequence *)allocator.allocate(sizeof(data_sync__srv__Trigger_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = data_sync__srv__Trigger_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
data_sync__srv__Trigger_Response__Sequence__destroy(data_sync__srv__Trigger_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    data_sync__srv__Trigger_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
data_sync__srv__Trigger_Response__Sequence__are_equal(const data_sync__srv__Trigger_Response__Sequence * lhs, const data_sync__srv__Trigger_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!data_sync__srv__Trigger_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
data_sync__srv__Trigger_Response__Sequence__copy(
  const data_sync__srv__Trigger_Response__Sequence * input,
  data_sync__srv__Trigger_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(data_sync__srv__Trigger_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    data_sync__srv__Trigger_Response * data =
      (data_sync__srv__Trigger_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!data_sync__srv__Trigger_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          data_sync__srv__Trigger_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!data_sync__srv__Trigger_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
