#!/bin/bash

# python3 -m pip install pylint

file_path=$1
file_url=$2
date=$3
time=$4
task_id=$5

echo "Src file: $file_path"
echo "URL: $file_url"
echo "Date of submission: $date $time"
echo "Hw id: $task_id"

echo "Linter output:"
pylint $file_path