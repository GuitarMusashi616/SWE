# Ty Bergstrom
# auto_train.py
# CSCE A401
# August 2020
# Software Engineering Project
#
# Build different models automatically and run continuously
# To test out different parameters and hypertuning for increased accuracy
#
# $ source ./venv1/bin/activate
# $ python3 auto_train.py


import os

# These args are mostly all of the different parameters you can add to a build for different hypertunings etc
models = ["-m Full_Net ", "-m Quick_Net "]
epochs = ["-e 25 ", "-e 50 ", "-e 75 ", "-e 100 "]
opt = ["-o Adam ", "-o Adam2 ", "-o Adam3 ", "-o Adam4 ", "-o SGD ", "-o SGD2 ", "-o SGD3 ", "-o RMSprop ", "-o Adadelta "]
aug = ["-a original ",  "-a light1 ", "-a light2 ", "-a light3 ", "-a medium1 ", "-a medium2 ", "-a medium3 ", "-a heavy1 ", "-a heavy2 "]
bs = ["-b xs ", "-b s ", "-b ms ", "-b m ", "-b lg ", "-b xlg "]
imgsz = ["-i xs ", "-i s ", "-i m ", "-i lg ", "-i xlg "]

# +ing the string args to this command
cmd = "python3 -W ignore train_a_model.py "
cmd += models[0]

# Save a plot of every build by +ing an iterator to the plot filepath
plot = "-p processing/plot"
i = 0

# Looping through the parameters you want to try out
for e in epochs[:1] :
    # Add epochs arg
    arg1 = cmd + e
    # And for every epoch setting, try a different batch size
    for b in [ bs[2], bs[3], bs[5] ] :
        plt = plot + str(i) + ".png "
        arg2 = arg1 + b + plt
        print("\n", arg2, "\n")
        os.system(arg2)
        i += 1


'''
for im in [ imgsz[1], imgsz[2] ] :
    arg1 = cmd + im
    for e in [ epochs[0], epochs[1] ] :
        arg2 = arg1 + e
        for b in bs:
            plt = plot + str(i) + ".png "
            arg3 = arg2 + b + plt
            print("\n", arg3, "\n")
            os.system(arg3)
            i += 1
'''


'''
i = 0
for im in [ imgsz[1], imgsz[3], imgsz[4] ] :
    arg = cmd + im
    for e in [ epochs[1], epochs[2] ] :
        arg1 = arg + e
        for o in [ opt[0], opt[1], opt[2], opt[6], opt[7], opt[4] ] :
            arg2 = arg1 + o
            for b in [ bs[6], bs[7], bs[8] ] :
                plt = plot + str(i) + ".png "
                arg3 = arg2 + str(b) + plt
                print("\n", arg3, "\n")
                os.system(arg3)
                plt = plot
                i += 1
'''



##
