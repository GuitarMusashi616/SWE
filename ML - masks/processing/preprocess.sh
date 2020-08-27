#!/bin/bash

# preprocess.sh
# Ty Bergstrom
# August 2020
#
# $ bash preprocess.sh
#
# This is a good pre-processing step to rename all files, get rid of weird internet filenames
# It helps in later processing steps when you need to find and manually process some images
#
# This was a need for a separate script to rename the image files in the original dataset directory
# And I wanted to try scripting this instead of python hacks
#
# Need to be very careful about renaming programmatically or you will accidentally delete lots of files
# This has been error check fairly well so that bad things don't happen
# But still it is good to backup your datasets before running anything like this
#
# Additionally afterwords this script can call the other python pre-processing scripts
# So you can run them all at once the way they are intended to run, see below
#
# You should manually rename any file that starts with "-" because commands don't like seeing that


cd ../original_dataset

# Manually define the directries - this can be done automatically, but want to be more careful
dirsArr=("test1" "test2")

# Err check that the directories exist before doing anything, can cause big problems
for val in "${!dirsArr[@]}"
do
    if [ -d "${dirsArr[$val]}" ]; then
        continue
    else
        printf "Err: The directory original_dataset/"${dirsArr[$val]}" does not exist"
        exit 1
    fi
done

for val in "${!dirsArr[@]}"
do
    # Make an empty temp directory - this implementation seems redundant but works much better & safer
    rm -rf tmp_dir
    mkdir tmp_dir
    printf "Working on "${dirsArr[$val]}" directory \n"
    cd "${dirsArr[$val]}"
    itr=0
    # Loop through all files in this directory
    for img_file in *
    do
        printf "Working on this file $img_file \n"
        # Get the extension
        ext=".${img_file##*.}"
        # Manually get the file type if there is no extension
        if [ $ext == ".$img_file" ]
            then
                if [ file --mime-type -b "$img_file" == "image/png" ]; then
                    ext=".png"
                elif [ file --mime-type -b "$img_file" == "image/jpeg" ]; then
                    ext=".jpg"
                else
                    ext=""
                fi
        fi
        # Copy to the temp directory, the renamed files are in the format /image_01.jpg
        printf "renaming to this file ../tmp_dir/image_"${itr}""${ext}" \n"
        # Err check that this file doesn't already exist, can really mess things up
        if [ -f "../tmp_dir/image_"${itr}""${ext}"" ]; then
            printf "Err: the file image_"${itr}""${ext}" already exists"
            # Just move over the original file name seems to solve it
            cp $img_file ../tmp_dir/$img_file
        else
            cp $img_file ../tmp_dir/image_"${itr}""${ext}"
        fi
        itr=$((itr+1))
    done
    cd ..
    # Remove the original directory with the weird filenames and replace it with the temp
    rm -rf "${dirsArr[$val]}"
    mv tmp_dir "${dirsArr[$val]}"
    rm -rf tmpdir
done

# Run the duplicate removing script
#python3 remove_duplicates.py -d original_dataset/mask
#python3 remove_duplicates.py -d original_dataset/without_mask

# Start fresh with empty directories for the processed datasets
#rm -rf processed_dataset/mask
#rm -rf processed_dataset/without_mask

# Run the script to find faces and save them in the processed datasets
#python3 process_faces.py -d mask
#python3 process_faces.py -d without_mask -o tru



##
