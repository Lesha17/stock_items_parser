#!/usr/bin/env bash

models/train.sh simple_cnn_characters_only exists_ru models/simple/characters_only/cnn/lstm.jsonnet
models/train.sh simple_cnn_characters_only_bidir exists_ru models/simple/characters_only/cnn/lstm_bidir.jsonnet
models/train.sh simple_cnn_characters_only_stacked_self_attention exists_ru models/simple/characters_only/cnn/stacked_self_attention.jsonnet

models/train.sh crf_cnn_characters_only exists_ru models/crf/characters_only/cnn/lstm.jsonnet
models/train.sh crf_cnn_characters_only_bidir exists_ru models/crf/characters_only/cnn/lstm_bidir.jsonnet
models/train.sh crf_cnn_characters_only_stacked_self_attention exists_ru models/crf/characters_only/cnn/stacked_self_attention.jsonnet
