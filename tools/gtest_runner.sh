#!/bin/bash

cd ../build
cmake ..
make

./runTests > result.txt
cat result.txt
