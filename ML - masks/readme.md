### CSCE A401 Software Engineering Group Project

### "Humanity's Last Hope"

## Machine Learning: detect wearing / not wearing masks

<br> 

```
Requirements:
tensorflow (1.5.0)
Keras (2.1.5)
opencv-python (4.2.0.32)
```

<br>

1. Data collection:

Save all images to `/original_data/mask` and `/original_data/without_mask`

Class labels are automatically handled by extracting from the file path of each image.

2a. Pre-processing:

Start by running `$ bash preprocess.sh`

The script begins by processing / organizing / renaming the image files for the entire dataset, does error checking, non-usable file types. Helps out a lot for later processing.

Then it calls `remove_duplicates.py` on each class directory. It generates hashes for each file and then removes files with duplicate hashes. Duplicates can cause bias, and you can end up with a lot of them.

Then it calls `process_faces.py` on each class directory.

    for each file:
        detect faces
        for each detected face:
            if detection probability is above threshold:
                crop the face and save it as a new 256 x 256 pixel image

Then you will have `/processed_data/mask` and `/processed_data/without_mask` that have images of just faces. The face detector works pretty well on detecting faces with masks.

Next you need to manually inspect the `processed_dataset/` and remove bad images that aren't a face, where the face detector didn't get it right. Find the original image and crop the face yourself (find them in the `original_dataset/` - they will have the same filenames to make it easier to find). 

`process_faces.py` will also save any images that detected zero faces to another directory `/processing/double_take` and you can go crop those faces manually. Manually save all of your manually cropped faces to the `processed_dataset/`. The goal is to make sure it's a good dataset with accurate data. The model will train with this dataset of cropped faces.

3. Training:

    - Model 1: Just show the 256x256 images of faces to the network and it will learn eventually.
    - Model 2: Cut the 256x256  face images in half, remove the top half, only send the bottom half through the network. Based on the observation that the bottom half contains most of mask/without_mask ROI. 
    - Model 3: Use the face detection coordinates for the nose/mouth/chin facial landmarks and make a cut out of the contour of the ROI and pass this through the model. Might be slower.

Then you can run `$ python3 train_a_model.py` 

It does some further processing, such as extracting and linking class labels with data, random train/test split, image resizing, scaling & normalizing, image_to_array, automatically handling enabling multiple class or binary classification, further processing for binary classifcation, etc. There are seven arguments for different hypertunings and parameters. This includes two neural network implemetation choices (a quicker lightweight net and a bigger deeper net), number of epochs, batch size, image size that the net will take, kernel size that the net will use, learning rate optimizer, processing augmentation. Then it does some standard compile and fit calls. Lastly it prints out some metrics and appends the metrics along with build parameters and info to a log, also saves a plot.

`auto_train.sh` just runs `train_a_model.py` over and over with as many build parameters as you wish with for loops - to try out lots of different hypertunings combinations. You can leave it running and check out the log to see which tunings get the best accuracy. It will fetch the five most accurate builds when it's done. It also saves all of the plots.

When you have determined the combination of tunings that get the best accuracy, save that model for production. A classification script will consult that model for predictions while reading from a video stream, or from input images.


4. Build an age prediction model. 

Without going too much into the detail, it's just another ML project. I would do a binary classification. Need images of children under the age of X and images of any and everyone older than X age. They should all be not wearing masks, as the goal is to exclude or whitelist children from the not-wearing-mask tag. Simply reuse most of the same pre-processing and neural nets (they are ready to use for any project), and train a model to predict whether an input face is under X age. Save the most accurate model, and then the classification script uses it to check whether a detected face that's not wearing a mask is a child.




<br> <br>



