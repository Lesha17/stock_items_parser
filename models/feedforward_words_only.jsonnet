// jsonnet allows local variables like this
local embedding_dim = 10;

local hidden_dims = [10, 20, 10];
local num_layers = 3;

local num_epochs = 100;
local patience = 10;
local batch_size = 20;
local learning_rate = 0.1;

{
    "dataset_reader": {
        "type": "custom-dataset-reader"
    },
    "model": {
        "type": "simple_tagger_f1",
        "text_field_embedder": {
            "token_embedders": {
                "tokens": {
                    "type": "embedding",
                    "embedding_dim": embedding_dim
                }
            }
        },
        "encoder": {
            "type": "feedforward",
            "feedforward": {
                "input_dim": embedding_dim,
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
            "type": "sgd",
            "lr": learning_rate
        },
        "patience": patience
    }
}