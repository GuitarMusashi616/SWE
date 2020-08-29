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
#1598664036.0856411 0.936364%
#1598664023.3946526 0.836364%
#1598664036.0856411 0.736364%
#1598664012.7201288 0.636364%
#1598664012.7201288 0.636364%

# Modify the -n arg if you want more than just the first best
head -n 1 tmp.txt > tmp2.txt
#1598664036.0856411 0.936364%

awk '{print $1}' tmp2.txt > tmp.txt
#1598664036.0856411

head tmp.txt | grep -A 3 -f - performance.txt
#build: 1598664036.0856411 0.736364%
#model: Full_Net, epochs: 15, optimzer: Adam, augmentation: original, 
#image size: 24, batch size: 16, kernel size: 3, dataset size: 110, run time: 10.75s
#notes: (none) 

rm tmp.txt
rm tmp2.txt



##
