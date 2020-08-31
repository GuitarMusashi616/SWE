#!/bin/bash

# preprocess.sh
# Ty Bergstrom
# August 2020
#
# $ bash preprocess.sh
#
# All in one pre-processing, the script will do some file renaming processing
# And then continue by running the other python files that do the rest of pre-processing
# So you can run them all at once the way they are intended to run, see below
#
# This is a good pre-processing step to rename all files, get rid of weird internet filenames
# It helps in later processing steps when you need to find and manually process some images
# Non-valid image types will be removed, such as .webp
#
# Need to be very careful about renaming programmatically or you will accidentally delete lots of files
# This has been error checked fairly well so that bad things don't happen
# But still it is good to backup your datasets before running anything like this
#
# You should manually rename any file that starts with "-" because commands don't like seeing that


cd ../original_dataset

# Manually define the directries - this can be done automatically, but want to be more careful
dirsArr=("mask" "without_mask")

# What do you want to rename the files as, change this if you are appending to a dataset
rename="image_"

# Err check that the directories exist before doing anything, can cause big problems
for val in "${!dirsArr[@]}"
do
    if [ ! -d "${dirsArr[$val]}" ]; then
        printf "Err: The directory original_dataset/"${dirsArr[$val]}" does not exist\m"
        exit 1
    fi
    # Also check for empty directories just because
    if [ ! "$(ls -A "${dirsArr[$val]}")" ]; then
        printf "Err: The directory original_dataset/"${dirsArr[$val]}" is empty\n"
        exit 1
    fi
done

for val in "${!dirsArr[@]}"
do
    # Make an empty temp directory - this implementation seems redundant but works better & safer
    rm -rf tmp_dir
    mkdir tmp_dir
    cd "${dirsArr[$val]}"
    # Just see what's in here first
    printf "Processing "${dirsArr[$val]}" directory \n"
    printf "ls -U | head -5\n"
    ls -U | head -5
    printf "ls | wc -l\n"
    ls | wc -l
    itr=0
    # Loop through all files in this directory
    for img_file in *
    do
        # Get the extension
        ext=".${img_file##*.}"
        # Manually get the file type if there is no extension
        if [ $ext == ".$img_file" ]; then
            # Update - these were all bad non-valid image types
            # Skipping them here will delete them which is better now than never
            continue
            if [[ $(file --mime-type -b "$img_file") == "image/png" ]]; then
                ext=".png"
            elif [[ $(file --mime-type -b "$img_file") == "image/jpeg" ]]; then
                ext=".jpg"
            else
                ext=""
            fi
        fi
        # Copy to the temp directory, the renamed files are in the format /image_01.jpg
        # Err check that this file doesn't already exist, can really mess things up
        if [ -f "../tmp_dir/"${rename}""${itr}""${ext}"" ]; then
            # Just move over the original file name seems to solve it
            cp "${img_file}" ../tmp_dir/$img_file
        else
            cp "${img_file}" ../tmp_dir/"${rename}""${itr}""${ext}"
        fi
        itr=$((itr+1))
    done
    # Just make sure that the directory did not end up empty before moving on, that could be bad
    if [ ! "$(ls -A ../tmp_dir/)" ]; then
        printf "Err: The directory original_dataset/"${dirsArr[$val]}" is empty\n"
        exit 1
    fi
    cd ..
    # Remove the original directory with the weird filenames and replace it with the temp
    rm -rf "${dirsArr[$val]}"
    mv tmp_dir "${dirsArr[$val]}"
    rm -rf tmpdir
    cd "${dirsArr[$val]}"
    # And see what ended up in here
    printf "ls -U | head -5\n"
    ls -U | head -5
    printf "ls | wc -l\n"
    ls | wc -l
    printf "\n"
    cd ..
done

cd ../processing

# These are the next steps of pre-processing
# Run everything from here to ensure consistency

# Run the duplicate removing script
printf "Removing duplicates...\n\n"
python3 remove_duplicates.py -d ../original_dataset/mask -r tru -s tru
python3 remove_duplicates.py -d ../original_dataset/without_mask -r tru -s tru

# Start fresh with empty directories for the processed datasets
start_fresh=1
if [ $start_fresh == 1 ]; then
    rm -rf ../processed_dataset/mask
    mkdir ../processed_dataset/mask
    rm -rf ../processed_dataset/without_mask
    mkdir ../processed_dataset/without_mask
    rm -rf double_take
    mkdir double_take
fi

# Run the script to find faces and save them in the processed datasets
printf "\nExtracting faces...\n\n"
python3 process_faces.py -d mask
python3 process_faces.py -d without_mask -o tru

printf "\Pre-processing complete!\n\n"



##
