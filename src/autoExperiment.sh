#! /bin/bash

# This is a quick bash script to run a set of experiments back to back so that you just have to 
# hit run and then just be done.

# ----------------------------------------- HOW TO RUN? ------------------------------------------
# run as follows:
# ./autoExperiment.sh [number] [N] [depth min] [depth max] [filename without .csv extension]

# ------------------------------------ WHAT DO THE ARGS MEAN? ------------------------------------
# [number] the number of the experiment you're running. For a quick explaination of what each 
# experiment is, please see the comments in runExperiment and the corresponding google doc

# [N] the total sample size you want the script to perform for each trial of a given depth. This 
# will be used in each row or trial, so please pick this number to not be huge less you want to
# run into issues during runtime

# [depth min] the minimum depth you're testing, the range we agreed on was 3 to 5, but there is no
# check for this, so you could very well just test more depths if your computer will allow you to 
# do so, and might give some interesting runtime in the future.

# [depth max] the maximum depth you're testing, this could be increased from the agreed depth but 
# might affect runtime in the future

# [filename] The name of the file you want to create and after it's created the shell script will 
# concat the rest of the data to the file. runExperiment already makes it a .csv already, so the
# extension is not needed to specify anything. It adds the .csv extention to make it more
# compatible and readible later without converting the file.

for ((i=${3}; i<=${4}; i++)); do
    echo $i;
    NUM=$((${3}+0));
    if (( $i == $NUM )); then 
        ./runExperiment ${1} ${2} $i ${5} 1 # Change here if you can't do runExperiment this way! DO NOT CHANGE PARAMETERS!
    else
        ./runExperiment ${1} ${2} $i ${5} 0 # Change here if you can't do runExperiment this way! DO NOT CHANGE PARAMETERS!
    fi
done