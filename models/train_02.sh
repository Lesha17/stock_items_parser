#!/usr/bin/env bash

models/train.sh cnn_ff_proj exists_ru/02 models/cnn_ff_proj.jsonnet 100
models/train.sh cnn_pt_crf exists_ru/02 models/cnn_pt_crf.jsonnet 100
models/train.sh cnn_lstm_proj exists_ru/02 models/cnn_lstm_proj.jsonnet 100
models/train.sh cnn_lstm_crf exists_ru/02 models/cnn_lstm_crf.jsonnet 100

models/train.sh lstm_ff_proj exists_ru/02 models/lstm_ff_proj.jsonnet 100
models/train.sh lstm_pt_crf exists_ru/02 models/lstm_pt_crf.jsonnet 100
models/train.sh lstm_lstm_proj exists_ru/02 models/lstm_lstm_proj.jsonnet 100
models/train.sh lstm_lstm_crf exists_ru/02 models/lstm_lstm_crf.jsonnet 100

models/train.sh cnn_ff_proj krepmarket/02 models/cnn_ff_proj.jsonnet 100
models/train.sh cnn_pt_crf krepmarket/02 models/cnn_pt_crf.jsonnet 100
models/train.sh cnn_lstm_proj krepmarket/02 models/cnn_lstm_proj.jsonnet 100
models/train.sh cnn_lstm_crf krepmarket/02 models/cnn_lstm_crf.jsonnet 100

models/train.sh lstm_ff_proj krepmarket/02 models/lstm_ff_proj.jsonnet 100
models/train.sh lstm_pt_crf krepmarket/02 models/lstm_pt_crf.jsonnet 100
models/train.sh lstm_lstm_proj krepmarket/02 models/lstm_lstm_proj.jsonnet 100
models/train.sh lstm_lstm_crf krepmarket/02 models/lstm_lstm_crf.jsonnet 100


