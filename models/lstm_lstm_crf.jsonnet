// jsonnet allows local variables like this
local char_embedding_dim = 20;
local word_embedding_dim = 20;
local encoder_input_dim = word_embedding_dim * 2;
local hidden_dim = 100;

local num_epochs = 80;
local patience = 10;
local batch_size = 100;
local learning_rate = 0.01;

{
    "dataset_reader": {
        "type": "custom-dataset-reader",
        "token_indexers": {
            "token_characters": { "type": "characters" }
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
                    "type": "lstm",
                    "input_size": char_embedding_dim,
                    "hidden_size": word_embedding_dim,
                    "bidirectional": true
                }
            }
        },
        "encoder": {
            "type": "lstm",
            "input_size": encoder_input_dim,
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
        "patience": patience,
        "validation_metric": "+f1_macro"
    }
}