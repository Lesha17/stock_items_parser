#!/usr/bin/env bash

models/eval.sh cnn_ff_proj exists_ru output/eval
models/eval.sh cnn_pt_crf exists_ru output/eval
models/eval.sh cnn_lstm_proj exists_ru output/eval
models/eval.sh cnn_lstm_crf exists_ru output/eval

models/eval.sh lstm_ff_proj exists_ru output/eval
models/eval.sh lstm_pt_crf exists_ru output/eval
models/eval.sh lstm_lstm_proj exists_ru output/eval
models/eval.sh lstm_lstm_crf exists_ru output/eval


