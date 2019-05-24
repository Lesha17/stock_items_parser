// jsonnet allows local variables like this
local embedding_dim = 6;
local hidden_dim = 6;
local num_epochs = 100;
local patience = 10;
local batch_size = 20;
local learning_rate = 0.1;

{
    "dataset_reader": {
        "type": "custom-dataset-reader"
    },
    "model": {
        "type": "simple_tagger",
        "text_field_embedder": {
            "token_embedders": {
                "tokens": {
                    "type": "embedding",
                    "embedding_dim": embedding_dim
                }
            }
        },
        "encoder": {
            "type": "lstm",
            "input_size": embedding_dim,
            "hidden_size": hidden_dim
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