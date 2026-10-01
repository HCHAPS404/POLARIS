# POLARIS C++20 placeholder kernel (P0). Not a hazard model.
cmake_minimum_required(VERSION 3.16)
project(polaris_placeholder LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(polaris_placeholder
  simulation/cpp/src/placeholder.cpp
)
target_include_directories(polaris_placeholder PUBLIC simulation/cpp/include)

add_executable(polaris_placeholder_test
  simulation/cpp/tests/test_placeholder.cpp
)
target_link_libraries(polaris_placeholder_test PRIVATE polaris_placeholder)

enable_testing()
add_test(NAME placeholder_add COMMAND polaris_placeholder_test)
