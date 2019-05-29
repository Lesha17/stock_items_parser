#!/usr/bin/env bash

# 0.0001

models/eval.sh cnn_ff_proj exists_ru/0_0001 output/eval
models/eval.sh cnn_pt_crf exists_ru/0_0001 output/eval
models/eval.sh cnn_lstm_proj exists_ru/0_0001 output/eval
models/eval.sh cnn_lstm_crf exists_ru/0_0001 output/eval

models/eval.sh lstm_ff_proj exists_ru/0_0001 output/eval
models/eval.sh lstm_pt_crf exists_ru/0_0001 output/eval
models/eval.sh lstm_lstm_proj exists_ru/0_0001 output/eval
models/eval.sh lstm_lstm_crf exists_ru/0_0001 output/eval

# 0.001

models/eval.sh cnn_ff_proj exists_ru/0_001 output/eval
models/eval.sh cnn_pt_crf exists_ru/0_001 output/eval
models/eval.sh cnn_lstm_proj exists_ru/0_001 output/eval
models/eval.sh cnn_lstm_crf exists_ru/0_001 output/eval

models/eval.sh lstm_ff_proj exists_ru/0_001 output/eval
models/eval.sh lstm_pt_crf exists_ru/0_001 output/eval
models/eval.sh lstm_lstm_proj exists_ru/0_001 output/eval
models/eval.sh lstm_lstm_crf exists_ru/0_001 output/eval

# 0.01

models/eval.sh cnn_ff_proj exists_ru/001 output/eval
models/eval.sh cnn_pt_crf exists_ru/001 output/eval
models/eval.sh cnn_lstm_proj exists_ru/001 output/eval
models/eval.sh cnn_lstm_crf exists_ru/001 output/eval

models/eval.sh lstm_ff_proj exists_ru/001 output/eval
models/eval.sh lstm_pt_crf exists_ru/001 output/eval
models/eval.sh lstm_lstm_proj exists_ru/001 output/eval
models/eval.sh lstm_lstm_crf exists_ru/001 output/eval

models/eval.sh cnn_ff_proj krepmarket/001 output/eval
models/eval.sh cnn_pt_crf krepmarket/001 output/eval
models/eval.sh cnn_lstm_proj krepmarket/001 output/eval
models/eval.sh cnn_lstm_crf krepmarket/001 output/eval

models/eval.sh lstm_ff_proj krepmarket/001 output/eval
models/eval.sh lstm_pt_crf krepmarket/001 output/eval
models/eval.sh lstm_lstm_proj krepmarket/001 output/eval
models/eval.sh lstm_lstm_crf krepmarket/001 output/eval

# 0.05

models/eval.sh cnn_ff_proj exists_ru/005 output/eval
models/eval.sh cnn_pt_crf exists_ru/005 output/eval
models/eval.sh cnn_lstm_proj exists_ru/005 output/eval
models/eval.sh cnn_lstm_crf exists_ru/005 output/eval

models/eval.sh lstm_ff_proj exists_ru/005 output/eval
models/eval.sh lstm_pt_crf exists_ru/005 output/eval
models/eval.sh lstm_lstm_proj exists_ru/005 output/eval
models/eval.sh lstm_lstm_crf exists_ru/005 output/eval

models/eval.sh cnn_ff_proj krepmarket/005 output/eval
models/eval.sh cnn_pt_crf krepmarket/005 output/eval
models/eval.sh cnn_lstm_proj krepmarket/005 output/eval
models/eval.sh cnn_lstm_crf krepmarket/005 output/eval

models/eval.sh lstm_ff_proj krepmarket/005 output/eval
models/eval.sh lstm_pt_crf krepmarket/005 output/eval
models/eval.sh lstm_lstm_proj krepmarket/005 output/eval
models/eval.sh lstm_lstm_crf krepmarket/005 output/eval

# 0.2

models/eval.sh cnn_ff_proj exists_ru/02 output/eval
models/eval.sh cnn_pt_crf exists_ru/02 output/eval
models/eval.sh cnn_lstm_proj exists_ru/02 output/eval
models/eval.sh cnn_lstm_crf exists_ru/02 output/eval

models/eval.sh lstm_ff_proj exists_ru/02 output/eval
models/eval.sh lstm_pt_crf exists_ru/02 output/eval
models/eval.sh lstm_lstm_proj exists_ru/02 output/eval
models/eval.sh lstm_lstm_crf exists_ru/02 output/eval

models/eval.sh cnn_ff_proj krepmarket/02 output/eval
models/eval.sh cnn_pt_crf krepmarket/02 output/eval
models/eval.sh cnn_lstm_proj krepmarket/02 output/eval
models/eval.sh cnn_lstm_crf krepmarket/02 output/eval

models/eval.sh lstm_ff_proj krepmarket/02 output/eval
models/eval.sh lstm_pt_crf krepmarket/02 output/eval
models/eval.sh lstm_lstm_proj krepmarket/02 output/eval
models/eval.sh lstm_lstm_crf krepmarket/02 output/eval

# 0.67

models/eval.sh cnn_ff_proj exists_ru/067 output/eval
models/eval.sh cnn_pt_crf exists_ru/067 output/eval
models/eval.sh cnn_lstm_proj exists_ru/067 output/eval
models/eval.sh cnn_lstm_crf exists_ru/067 output/eval

models/eval.sh lstm_ff_proj exists_ru/067 output/eval
models/eval.sh lstm_pt_crf exists_ru/067 output/eval
models/eval.sh lstm_lstm_proj exists_ru/067 output/eval
models/eval.sh lstm_lstm_crf exists_ru/067 output/eval

models/eval.sh cnn_ff_proj krepmarket/067 output/eval
models/eval.sh cnn_pt_crf krepmarket/067 output/eval
models/eval.sh cnn_lstm_proj krepmarket/067 output/eval
models/eval.sh cnn_lstm_crf krepmarket/067 output/eval

models/eval.sh lstm_ff_proj krepmarket/067 output/eval
models/eval.sh lstm_pt_crf krepmarket/067 output/eval
models/eval.sh lstm_lstm_proj krepmarket/067 output/eval
models/eval.sh lstm_lstm_crf krepmarket/067 output/eval
