set(_AMENT_PACKAGE_NAME "odrive_can")
set(odrive_can_VERSION "0.0.1")
set(odrive_can_MAINTAINER "root <nicholas.schneider@odriverobotics.com>")
set(odrive_can_BUILD_DEPENDS "ament_cmake" "rosidl_default_generators" "rclcpp" "std_srvs")
set(odrive_can_BUILDTOOL_DEPENDS "ament_cmake")
set(odrive_can_BUILD_EXPORT_DEPENDS "rclcpp" "std_srvs")
set(odrive_can_BUILDTOOL_EXPORT_DEPENDS )
set(odrive_can_EXEC_DEPENDS "ament_cmake" "rosidl_default_runtime" "rclcpp" "std_srvs")
set(odrive_can_TEST_DEPENDS "ament_lint_auto" "ament_lint_common")
set(odrive_can_GROUP_DEPENDS )
set(odrive_can_MEMBER_OF_GROUPS "rosidl_interface_packages")
set(odrive_can_DEPRECATED "")
set(odrive_can_EXPORT_TAGS)
list(APPEND odrive_can_EXPORT_TAGS "<rosidl_package_name>${PROJECT_NAME}</rosidl_package_name>")
list(APPEND odrive_can_EXPORT_TAGS "<rosidl_target_interfaces>msg/${PROJECT_NAME}.msg</rosidl_target_interfaces>")
list(APPEND odrive_can_EXPORT_TAGS "<build_type>ament_cmake</build_type>")
