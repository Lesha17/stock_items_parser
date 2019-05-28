#!/usr/bin/env bash

# 1 - model name
# 2 - dataset name
# 3 -output file

mkdir -p $3/$2
allennlp evaluate output/models/$1/$2/ --include-package layers -o '{"model":{"verbose_metrics": true}}' temp/datasets/$2/$2_train.xlsx --output-file $3/$2/$1_train.txt
allennlp evaluate output/models/$1/$2/ --include-package layers -o '{"model":{"verbose_metrics": true}}' temp/datasets/$2/$2_test.xlsx --output-file $3/$2/$1_test.txt
allennlp evaluate output/models/$1/$2/ --include-package layers -o '{"model":{"verbose_metrics": true}}' temp/datasets/$2/$2_validate_test.xlsx --output-file $3/$2/$1_validate_test.txt
