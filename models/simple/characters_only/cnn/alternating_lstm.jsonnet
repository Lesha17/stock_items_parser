// jsonnet allows local variables like this
local char_embedding_dim = 20;
local word_embedding_dim = 80;
local encoder_input_dim = word_embedding_dim;
local hidden_dim = 100;
local num_layers = 3;

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
        "type": "simple_tagger_f1",
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
                    "output_dim": word_embedding_dim
                }
            }
        },
        "encoder": {
            "type": "alternating_lstm",
            "input_size": encoder_input_dim,
            "hidden_size": hidden_dim,
            "num_layers": num_layers
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