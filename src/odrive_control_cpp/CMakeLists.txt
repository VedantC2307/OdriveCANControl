cmake_minimum_required(VERSION 3.8)
project(odrive_control_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(odrive_can REQUIRED)

# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

# Add executables
add_executable(control_node src/control_node.cpp)
ament_target_dependencies(control_node rclcpp std_msgs odrive_can)

add_executable(subscribe_send src/subscribe_send.cpp)
ament_target_dependencies(subscribe_send rclcpp std_msgs odrive_can)

add_executable(receive_send src/receive_send.cpp)
ament_target_dependencies(receive_send rclcpp std_msgs odrive_can)

install(TARGETS
  control_node
  subscribe_send
  receive_send
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
