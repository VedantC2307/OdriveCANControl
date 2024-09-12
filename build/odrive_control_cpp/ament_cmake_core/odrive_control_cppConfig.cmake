# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_odrive_control_cpp_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED odrive_control_cpp_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(odrive_control_cpp_FOUND FALSE)
  elseif(NOT odrive_control_cpp_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(odrive_control_cpp_FOUND FALSE)
  endif()
  return()
endif()
set(_odrive_control_cpp_CONFIG_INCLUDED TRUE)

# output package information
if(NOT odrive_control_cpp_FIND_QUIETLY)
  message(STATUS "Found odrive_control_cpp: 0.0.0 (${odrive_control_cpp_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'odrive_control_cpp' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${odrive_control_cpp_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(odrive_control_cpp_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${odrive_control_cpp_DIR}/${_extra}")
endforeach()
