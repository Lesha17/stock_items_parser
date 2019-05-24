#!/usr/bin/env bash


allennlp evaluate output/models/crf_lstm_with_characters/exists_ru/ temp/datasets/exists_ru/exists_ru_other.xlsx --include-package layers --extend-vocab
