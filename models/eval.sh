#!/usr/bin/env bash

# 1 - model name
# 2 - dataset name
# 3 -output file

mkdir -p $3/$1/$2
allennlp evaluate output/models/$2/$1/ --include-package layers -o '{"model":{"verbose_metrics": true}}' temp/datasets/$2/train.xlsx --output-file $3/$1/$2/train.txt
allennlp evaluate output/models/$2/$1/ --include-package layers -o '{"model":{"verbose_metrics": true}}' temp/datasets/$2/test.xlsx --output-file $3/$1/$2/test.txt
allennlp evaluate output/models/$2/$1/ --include-package layers -o '{"model":{"verbose_metrics": true}}' temp/datasets/$2/other.xlsx --output-file $3/$1/$2/validate.txt
