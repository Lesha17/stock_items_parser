#!/usr/bin/env bash


allennlp evaluate output/models/crf_lstm_characters_only/exists_ru/ --include-package layers -o '{"model":{"verbose_metrics": true}}' temp/datasets/exists_ru/exists_ru_other.xlsx
