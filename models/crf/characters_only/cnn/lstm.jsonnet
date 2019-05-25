// jsonnet allows local variables like this
local char_embedding_dim = 20;
local word_embedding_dim = 40;
local hidden_dim = 60;

local num_epochs = 100;
local patience = 10;
local batch_size = 100;
local learning_rate = 0.1;

{
    "dataset_reader": {
        "type": "custom-dataset-reader",
        "token_indexers": {
            "token_characters": {
                "type": "characters",
                "min_padding_length": 3
            }
        }
    },
    "model": {
        "type": "crf_tagger_f1",
        "text_field_embedder": {
            "token_characters": {
                "type": "character_encoding",
                "embedding": {
                    "embedding_dim": char_embedding_dim,
                },
                "encoder": {
                    "type": "cnn",
                    "embedding_dim": char_embedding_dim,
                    "num_filters": 20,
                    "output_dim": word_embedding_dim,
                    "ngram_filter_sizes": [2, 3]
                }
            }
        },
        "encoder": {
            "type": "lstm",
            "input_size": word_embedding_dim,
            "hidden_size": hidden_dim,
            "bidirectional": true
        }
    },
    "iterator": {
        "type": "basic",
        "batch_size": batch_size
    },
    "trainer": {
        "num_epochs": num_epochs,
        "optimizer": {
            "type": "adam",
            "lr": learning_rate
        },
        "patience": patience
    }
}