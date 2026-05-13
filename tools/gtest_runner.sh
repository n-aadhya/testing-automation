#!/bin/bash

echo "Deleting old coverage files..."
find . -name "*.gcda" -delete
find . -name "*.gcno" -delete

mkdir -p ../build
cd ../build || exit

cmake ..
make

echo "Running tests..."
./runTests

echo "Capturing coverage..."

lcov --rc branch_coverage=1 \
     --capture \
     --directory . \
     --output-file coverage.info

echo "Filtering coverage..."

lcov --remove coverage.info \
    '/usr/*' \
    '*/googletest/*' \
    '*/tests/*' \
    -o filtered.info

echo "Coverage Summary"

lcov --rc branch_coverage=1 \
     --summary filtered.info
