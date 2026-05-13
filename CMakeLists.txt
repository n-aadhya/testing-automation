cmake_minimum_required(VERSION 3.10)

project(UnitTestProject)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-arcs -ftest-coverage")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fprofile-arcs -ftest-coverage")

add_executable(runTests
    src/max3.cpp
    tests/test_generated.cpp
)

target_link_libraries(runTests
    gtest
    gtest_main
    pthread
)
