cmake_minimum_required(VERSION 3.10)
project(UnitTestProject)

# Enable coverage flags BEFORE target creation
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --coverage")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --coverage")

add_executable(runTests
    src/max3.cpp
    tests/test_generated.cpp
)

target_link_libraries(runTests gtest gtest_main pthread)
