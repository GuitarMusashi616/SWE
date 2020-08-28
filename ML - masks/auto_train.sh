#!/bin/bash

# bash auto_train.sh
#
# Same as auto_train.py
# Wanted to see how it would be implemented in bash
# This looks better


models=("-m Full_Net " "-m Quick_Net ")
epochs=("-e 25 " "-e 50 " "-e 75 " "-e 100 ")
opt=("-o Adam " "-o Adam2 " "-o Adam3 " "-o Adam4 " "-o SGD " "-o SGD2 " "-o SGD3 " "-o RMSprop " "-o Adadelta ")
aug=("-a original "  "-a light1 " "-a light2 " "-a light3 " "-a medium1 " "-a medium2 " "-a medium3 " "-a heavy1 " "-a heavy2 ")
bs=("-b xs " "-b s " "-b ms " "-b m " "-b lg " "-b xlg ")
imgsz=("-i xs " "-i s " "-i m " "-i lg " "-i xlg ")
kernel=("-k 3" "-k 5")

source ./venv1/bin/activate

cmd="python3 -W ignore train_a_model.py -d original_dataset"

itr=0

# Loop thru optimizers
for o in "${!opt[@]}"
do
    # Loop thru number epochs
    for e in "${!epochs[@]}"
    do
        # Loop thru batch sizes
        for b in "${!bs[@]}"
        do
            # Loop thru image sizes
            for i in "${!imgsz[@]}"
            do

                $cmd ${models[0]} ${opt[$o]} ${epochs[$e]} ${bs[$b]} ${imgsz[$i]} "-p processing/plot_"${itr}".png"
                printf " $cmd ${models[0]} ${opt[$o]} ${epochs[$e]} ${bs[$b]} ${imgsz[$i]} -p processing/plot_${itr}.png "
                itr=$((itr+1))

            done # image sizes
        done # batch sizes
    done # number of epochs
done # optimizers



##
