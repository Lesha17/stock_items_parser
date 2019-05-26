#!/usr/bin/env bash

models/eval.sh crf_lstm_characters_only exists_ru $1
models/eval.sh crf_lstm_characters_only_bidir exists_ru $1
models/eval.sh crf_lstm_characters_only_feedforward exists_ru $1
models/eval.sh crf_lstm_characters_only_multi_head_self_attention exists_ru $1
models/eval.sh crf_lstm_characters_only_bidirectional_language_model_transformer exists_ru $1
models/eval.sh crf_lstm_characters_only_qanet_encoder exists_ru $1

models/eval.sh crf_lstm_characters_only_stacked_bidirectional_lstm exists_ru $1
models/eval.sh crf_lstm_characters_only_stacked_self_attention exists_ru $1
models/eval.sh crf_lstm_characters_only_alternating_lstm exists_ru $1
models/eval.sh crf_lstm_characters_only_alternating_lstm exists_ru $1
models/eval.sh crf_lstm_characters_only_augmented_lstm exists_ru $1

models/eval.sh simple_lstm_characters_only exists_ru $1
models/eval.sh simple_lstm_characters_only_bidir exists_ru $1
models/eval.sh simple_lstm_characters_only_feedforward exists_ru $1
models/eval.sh simple_lstm_characters_only_multi_head_self_attention exists_ru $1
models/eval.sh simple_lstm_characters_only_bidirectional_language_model_transformer exists_ru $1
models/eval.sh simple_lstm_characters_only_qanet_encoder exists_ru $1

models/eval.sh simple_lstm_characters_only_stacked_bidirectional_lstm exists_ru $1
models/eval.sh simple_lstm_characters_only_stacked_self_attention exists_ru $1
models/eval.sh simple_lstm_characters_only_alternating_lstm exists_ru $1
models/eval.sh simple_lstm_characters_only_augmented_lstm exists_ru $1