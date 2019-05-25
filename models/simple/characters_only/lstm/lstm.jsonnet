// jsonnet allows local variables like this
local char_embedding_dim = 10;
local word_embedding_dim = 40;
local encoder_input_dim = word_embedding_dim;
local hidden_dims = [50, 50, 50];
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
                    "type": "lstm",
                    "input_size": char_embedding_dim,
                    "hidden_size": word_embedding_dim
                }
            }
        },
        "encoder": {
            "type": "feedforward",
            "feedforward": {
                "input_dim": encoder_input_dim,
                "num_layers": num_layers,
                "hidden_dims": hidden_dims,
                "activations": "linear"
            }
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