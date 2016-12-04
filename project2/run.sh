#!/bin/bash
echo "Simulating N:30 A:6 P:1.0"
python simtest_persistent.py 30 6 1.0

echo "Simulating N:30 A:6 P:0.1"
python simtest_persistent.py 30 6 0.1

echo "Simulating N:30 A:6 P:0.01"
python simtest_persistent.py 30 6 0.01

echo "Simulating N:30 A:7 P:1.0"
python simtest_persistent.py 30 7 1.0

echo "Simulating N:30 A:7 P:0.1"
python simtest_persistent.py 30 7 0.1

echo "Simulating N:30 A:7 P:0.01"
python simtest_persistent.py 30 7 0.01

echo "Simulating N:30 A:8 P:1.0"
python simtest_persistent.py 30 8 1.0

echo "Simulating N:30 A:8 P:0.1"
python simtest_persistent.py 30 8 0.1

echo "Simulating N:30 A:8 P:0.01"
python simtest_persistent.py 30 8 0.01

echo "Simulating N:30 A:9 P:1.0"
python simtest_persistent.py 30 9 1.0

echo "Simulating N:30 A:9 P:0.1"
python simtest_persistent.py 30 9 0.1

echo "Simulating N:30 A:9 P:0.01"
python simtest_persistent.py 30 9 0.01
