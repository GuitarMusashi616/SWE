#!/bin/bash
#
# Ty Bergstrom
# best_acc.sh
# CSCE A401
# August 2020
# Software Engineering Project
#
# bash best_acc.sh
#
# The linux commands to extract the most accurate build parameters from the performance log


grep build performance.txt | sort -k 3 -nr | head -5 | awk '{print $2 " " $3}' > tmp.txt

head -n 1 tmp.txt > tmp2.txt

awk '{print $1}' tmp2.txt > tmp.txt

head tmp.txt | grep -A 3 -f - performance.txt

rm tmp.txt
rm tmp2.txt



##
