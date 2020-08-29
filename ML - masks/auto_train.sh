#!/bin/bash
#
# Ty Bergstrom
# auto_train.sh
# CSCE A401
# August 2020
# Software Engineering Project
#
# bash auto_train.sh
#
# Build different models automatically and run continuously
# Using for loops to try different combinations of build parameters
# To test out different hypertunings for increased accuracy


models=("-m Full_Net " "-m Quick_Net ")
epochs=("-e 25 " "-e 50 " "-e 75 " "-e 100 ")
opt=("-o Adam " "-o Adam2 " "-o Adam3 " "-o Adam4 " "-o SGD " "-o SGD2 " "-o SGD3 " "-o RMSprop " "-o Adadelta ")
aug=("-a original "  "-a light1 " "-a light2 " "-a light3 " "-a medium1 " "-a medium2 " "-a medium3 " "-a heavy1 " "-a heavy2 ")
bs=("-b xs " "-b s " "-b ms " "-b m " "-b lg " "-b xlg ")
imgsz=("-i xs " "-i s " "-i m " "-i lg " "-i xlg ")
kernel=("-k 3" "-k 5")

source ./venv1/bin/activate

now=`date`
printf "\n\n** Beginning auto_train.sh on $now\n\n" >> processing/performance.txt

cmd="python3 -W ignore train_a_model.py -d original_dataset"
plot="-p processing/plots/plot"

itr=0

# Loop thru optimizers
for o in "${!opt[@]}"
do
     Loop thru number epochs
    for e in "${!epochs[@]}"
    do
        # Loop thru batch sizes
        for b in "${!bs[@]}"
        do
            # Loop thru image sizes
            for i in "${!imgsz[@]}"
            do

                printf "\n $cmd ${models[0]} ${opt[$o]} ${epochs[$e]} ${bs[$b]} ${imgsz[$i]}-p processing/plots/plot${itr}.png \n"
                $cmd ${models[0]} ${opt[$o]} ${epochs[$e]} ${bs[$b]} ${imgsz[$i]} ${plot}${itr}".png"
                itr=$((itr+1))

            done # image sizes
        done # batch sizes
    done # number of epochs
done # optimizers

echo Finished auto_train.sh on $now >> processing/performance.txt

# List the 5 builds with the highest accuracy
grep build processing/performance.txt | sort -k 3 -nr | head -5 | awk '{print $2 " " $3}' >> processing/performance.txt



##
