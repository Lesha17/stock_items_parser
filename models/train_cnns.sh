#!/usr/bin/env bash

models/train.sh cnn_ff_proj exists_ru models/cnn_ff_proj.jsonnet
models/train.sh cnn_pt_crf exists_ru models/cnn_pt_crf.jsonnet
models/train.sh cnn_lstm_proj exists_ru models/cnn_lstm_proj.jsonnet
models/train.sh cnn_lstm_crf exists_ru models/cnn_lstm_crf.jsonnet

