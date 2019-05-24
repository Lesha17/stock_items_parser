#!/usr/bin/env bash


# 1 - model name
# 2 - dataset name
# 3 - model config path

# Make full vocabulary - for labels
rm -rf temp/datasets/$2/$1/*
allennlp make-vocab $3 -s temp/datasets/$2/$1/ --include-package layers -o '{"train_data_path":'"'"'temp/datasets/'$2/$2'_train.xlsx'"'"',"validation_data_path":'"'"'temp/datasets/'$2/$2'_other.xlsx'"'"'}'

rm temp/labels.txt
mv temp/datasets/$2/$1/vocabulary/labels.txt temp

# Make vocabulary - just for train words
rm -rf temp/datasets/$2/$1/*
allennlp make-vocab $3 -s temp/datasets/$2/$1/ --include-package layers -o '{"train_data_path":'"'"'temp/datasets/'$2/$2'_train.xlsx'"'"',"validation_data_path":null}'

# Finally move labels back
rm temp/datasets/$2/$1/vocabulary/labels.txt
mv temp/labels.txt temp/datasets/$2/$1/vocabulary/labels.txt

# Train
rm -rf output/models/$1/$2/*
allennlp train $3 -s output/models/$1/$2 --include-package layers -o '{"train_data_path":'"'"'temp/datasets/'$2/$2'_train.xlsx'"'"',"validation_data_path":'"'"'temp/datasets/'$2/$2'_test.xlsx'"'"',"vocabulary": {"directory_path":'"'"'temp/datasets/'$2/$1'/vocabulary'"'"' }}'
