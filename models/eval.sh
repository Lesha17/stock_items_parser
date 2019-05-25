#!/usr/bin/env bash

# 1 - model name
# 2 - dataset name
# 3 -output file

mkdir -p $3/$2
allennlp evaluate output/models/$1/$2/ --include-package layers -o '{"model":{"verbose_metrics": true}}' temp/datasets/$2/$2_other.xlsx --output-file $3/$2/$1.txt
