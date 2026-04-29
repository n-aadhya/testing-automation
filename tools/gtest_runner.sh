#!/bin/bash

cd ../build

# reset coverage
lcov --directory . --zerocounters

cmake ..
make

./runTests

# capture coverage
lcov --capture --directory . --output-file coverage.info

# summary
lcov --summary coverage.info > coverage.txt

cat coverage.txt
