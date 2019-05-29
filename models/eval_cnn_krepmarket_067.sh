#!/usr/bin/env bash

models/eval.sh cnn_ff_proj krepmarket/067 output/eval
models/eval.sh cnn_pt_crf krepmarket/067 output/eval
models/eval.sh cnn_lstm_proj krepmarket/067 output/eval
models/eval.sh cnn_lstm_crf krepmarket/067 output/eval

