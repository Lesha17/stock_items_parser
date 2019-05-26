#!/usr/bin/env bash

models/train.sh lstm_ff_proj exists_ru models/lstm_ff_proj.jsonnet
models/train.sh lstm_pt_crf exists_ru models/lstm_pt_crf.jsonnet
models/train.sh lstm_lstm_proj exists_ru models/lstm_lstm_proj.jsonnet
models/train.sh lstm_lstm_crf exists_ru models/lstm_lstm_crf.jsonnet

