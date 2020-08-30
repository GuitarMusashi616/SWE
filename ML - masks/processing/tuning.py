# Ty Bergstrom
# tuning.py
# CSCE A401
# August 2020
# Software Engineering Project
#
# Hypertuning for any model
# Makes more efficient testing different parameters for increased accuracy
# Choose these parameters from terminal args or for loops
# Instead of crazy editing and commenting out all over the place


from keras.callbacks import LearningRateScheduler
#import tensorflow_model_optimization as tfmot
#from keras.optimizers import schedules
from keras.optimizers import Adadelta
from keras.optimizers import RMSprop
from keras.optimizers import Adam
from keras.optimizers import SGD
from nets.net import Quick_Net
from nets.net import Full_Net
from collections import OrderedDict


class Tune:

    # Choose among the neural net implementations
    def build_model(mod, HXW, channels, kernel, num_classes):
        models = [
            "Quick_Net",
            "Full_Net"
        ]
        if mod == models[1]:
            return Full_Net.build(width=HXW, height=HXW, depth=channels, kernel=kernel, classes=num_classes)
        return Quick_Net.build(width=HXW, height=HXW, depth=channels, kernel=kernel, classes=num_classes)


    # Pre-set optimizers for learning rates
    def optimizer(opt, epochs):
        if opt == "Adam":
            return Adam(lr=0.001, decay=0.001/epochs)
        elif opt == "Adam2":
            return Adam(lr=0.001, beta_1=0.9, beta_2=0.999)
        elif opt == "Adam3":
            return Adam(lr=0.001, beta_1=0.9, beta_2=0.999, amsgrad=True)
        elif opt == "Adam4":
            return Adam(lr=0.001, decay=0.001/epochs, amsgrad=True)
        elif opt == "SGD":
            return SGD(lr=0.1, decay=0.1, momentum=0.01, nesterov=True)
        elif opt == "SGD2":
            return SGD(lr=0.1, decay=0.1, momentum=0.05, nesterov=True)
        elif opt == "SGD3":
            return SGD(lr=0.1, decay=0.1, momentum=0.1, nesterov=True)
        elif opt == "RMSprop":
            return RMSprop(lr=0.001, rho=0.9)
        elif opt == "Adadelta":
            return Adadelta(lr=1.0, rho=0.9)
        else:
            return Adam(lr=0.001)


    # Pre-set batch sizes (*too large will crash)
    def batch_size(size):
        batch_sizes = OrderedDict([
	        ("xs", 16),
	        ("s", 24),
	        ("ms", 32),
	        ("m", 42),
	        ("lg", 64),
	        ("xlg", 72),
        ])
        # Error checking, return default or a custom size
        if size not in batch_sizes:
            if isinstance(size, int) and size >= 8 and size <= 512:
                return int(size)
            else:
                return batch_sizes[ms]
        return batch_sizes[size]


    # Pre-set image sizes to feed to the model (*too large will crash)
    def img_size(size):
        img_sizes = OrderedDict([
	        ("xs", 24),
	        ("s", 32),
	        ("m", 48),
	        ("lg", 64),
	        ("xlg", 72),
        ])
        # Error checking, return default
        if size not in img_sizes:
            return img_sizes[s]
        return img_sizes[size]


    # Pre-set kernel sizes, really only error checking, don't want anything else than 3 or 5
    def kernel(size):
        if size == 5:
            return 5
        return 3


    # Call to Keras fit_generator() library, placed here for cleaner code and encapsulation
    def fit(model, aug, num_epochs, bs, train_X, train_Y, test_X, test_Y):
        # Some of these are extra hyperparameters to modified
        H = model.fit_generator(
            aug.flow(train_X, train_Y, batch_size=bs),
            validation_data=(test_X, test_Y),
            steps_per_epoch=len(train_X) // bs,
            epochs=num_epochs,
            class_weight=[1.0,1.0],
            shuffle=False,
            verbose=2
        )
        return H


    # Really just an error check for valid range of epochs
    def epoch(epochs):
        if epochs >= 1 and epochs <= 200:
            return epochs
        return 1


    # Customized learning rates, not currently supported
    def lr_sched(decay, epochs):
        def step_decay(epoch):
            init_lr = 0.1
            drop = 0.5
            epoch_drop = 10.0
            lr = init_lr * math.pow(drop, math.floor((1 + epoch) / epoch_drop))
            return lr
        def poly_decay(epoch):
	        maxEpochs = epochs
	        init_lr = 0.1
	        power = 1.1
	        alpha = init_lr * (1 - (epoch / float(maxEpochs))) ** power
	        return alpha
        if decay == "step":
            return [LearningRateScheduler(step_decay)]
        elif decay == "polynomial":
            return [LearningRateScheduler(poly_decay)]
        elif decay == "reduce":
            lr = ReduceLROnPlateau(monitor='val_acc', patience=5,
                verbose=1, factor=0.5, min_lr=0.0001)
            return [lr]


    '''
    # Pruning the model currently not supported
    def prune(model):
        pruning_schedule = tfmot.sparsity.keras.PolynomialDecay(initial_sparsity=0.0, 
            final_sparsity=0.5, begin_step=2000, end_step=4000)
        return tfmot.sparsity.keras.prune_low_magnitude(model, pruning_schedule=pruning_schedule)
    '''



##
