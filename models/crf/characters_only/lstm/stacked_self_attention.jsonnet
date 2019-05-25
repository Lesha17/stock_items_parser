// jsonnet allows local variables like this
local char_embedding_dim = 10;
local word_embedding_dim = 40;
local encoder_input_dim = word_embedding_dim * 2;
local hidden_dim = 50;

local num_epochs = 100;
local patience = 10;
local batch_size = 100;
local learning_rate = 0.1;

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
            "type": "stacked_self_attention",
            "input_dim": encoder_input_dim,
            "projection_dim": 10,
            "hidden_dim": hidden_dim,
            "feedforward_hidden_dim": hidden_dim,
            "num_layers": 3,
            "num_attention_heads": 2
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