#!/usr/bin/env bash


# 1 - model name
# 2 - dataset name
# 3 - model config path

# Train
rm -rf output/models/$2/$1/*
allennlp train $3 -s output/models/$2/$1 --include-package layers -o '{"train_data_path":'"'"'temp/datasets/'$2'/train.xlsx'"'"',"validation_data_path":'"'"'temp/datasets/'$2'/test.xlsx'"'"'}'
