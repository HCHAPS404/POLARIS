# POLARIS C++20 kernel (P0 placeholder + P6 event scheduler). Not a hazard model.
cmake_minimum_required(VERSION 3.16)
project(polaris_cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(BUILD_PYBIND11_BINDINGS "Build pybind11 module polaris_event_scheduler" OFF)

add_library(polaris_core
  simulation/cpp/src/placeholder.cpp
  simulation/cpp/src/event_scheduler.cpp
)
target_include_directories(polaris_core PUBLIC simulation/cpp/include)

add_executable(polaris_placeholder_test
  simulation/cpp/tests/test_placeholder.cpp
)
target_link_libraries(polaris_placeholder_test PRIVATE polaris_core)

add_executable(polaris_event_scheduler_test
  simulation/cpp/tests/test_event_scheduler.cpp
)
target_link_libraries(polaris_event_scheduler_test PRIVATE polaris_core)

enable_testing()
add_test(NAME placeholder_add COMMAND polaris_placeholder_test)
add_test(NAME event_scheduler_order COMMAND polaris_event_scheduler_test)

if(BUILD_PYBIND11_BINDINGS)
  include(FetchContent)
  FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG v2.13.6
  )
  FetchContent_MakeAvailable(pybind11)

  pybind11_add_module(polaris_event_scheduler simulation/bindings/event_scheduler_module.cpp)
  target_link_libraries(polaris_event_scheduler PRIVATE polaris_core)
endif()
