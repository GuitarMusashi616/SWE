1. Data collection:

Save all images to `/original_data/mask` and `/original_data/without_mask`

Class labels are automatically handled by extracting from the file path of each image.

2. Pre-processing:

`preprocess.sh` begins by processing / organizing / renaming the image files for the entire dataset, does error checking, deletes non image files. Helps out a lot for later processing.

Then it calls `remove_duplicates.py` on each class directory. It generates hashes for each file and then removes files with duplicate hashes. Duplicates can cause bias.

Then it calls `process_faces.py` on each class directory.

    for each file:
        detect faces
        for each detected face:
            if face is above probability threshold:
                crop the face and save it as a new 256 x 256 pixel image

Then you will have `/processed_data/mask` and `/processed_data/without_mask` that have images of just faces. The face detector works pretty well on detecting faces with masks.

Next you need to manually pre-process the data. Manually inspect the `processed_dataset` and remove bad images that aren't a face. Find the original image and crop the face yourself. `process_faces.py` will also save any images that detected zero faces to another directory and you can go crop those faces manually. Make sure it's a good dataset with accurate data. The model will train with this dataset of cropped faces.

3. Training:

`train_a_model.py` does it all. It does some further processing, such as extracting and linking labels and data, random train/test split, image resizing, scaling, image_to_array, automatically handling enabling multiple class or binary classification, further processing for binary classifcation, etc. There are seven arguments for differnt hypertunings and parameters. This includes two neural network implemetation choices, number of epochs, batch size, image size that the net will take, kernal size that the net will use, learning rate optimizer, processing augmentation. Then it does some standard compile and fit calls. Lastly it prints out some metrics and appends the metrics along with build parameters and info to a log, also saves a plot.

`auto_train.py` just runs `train_a_model.py` with as many build parameters as you wish with for loops to try out many different hypertunings. You can leave it running and check out the log to see which tunings get the best accuracy. 
