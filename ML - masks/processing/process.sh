#!/bin/bash

# process.sh
# Ty Bergstrom
# August 2020
#
# $ bash process.sh
#
# This is a good pre-processing step to rename all files
# It helps in later processing steps when you need to find and manually process some images
#
# Need to be careful about renaming programmatically or you will accidentally delete lots of files
# This script carefully renames the image files, preserving extensions
# Deletes the originals and does not make backups
#
# I make a copies of my original datasets before I do anything like this just to be sure
#
# After renaming, it runs the pythons script that searches for and removes duplicate images on every directory
# Then it runs the face processing script
# So run this script when you're ready to do all the processing at once
# Or also this is the only script you need to run if whenever you (regularly) update your databases


cd ../original_dataset

# Manually define the directries - this can be done automatically, but want to be more careful
dirsArr=("test1" "test2")
for val in "${!dirsArr[@]}"
do
    # Make an empty temp directory
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
        cp $img_file ../tmp_dir/image_"${itr}""${ext}"
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
