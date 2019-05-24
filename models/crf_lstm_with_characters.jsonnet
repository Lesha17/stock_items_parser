// jsonnet allows local variables like this
local word_embedding_dim = 6;
local char_embedding_dim = 3;
local embedding_dim = word_embedding_dim + char_embedding_dim;
local hidden_dim = 6;
local num_epochs = 100;
local patience = 10;
local batch_size = 20;
local learning_rate = 0.1;

{
    "dataset_reader": {
        "type": "custom-dataset-reader",
        "token_indexers": {
            "tokens": { "type": "single_id" },
            "token_characters": { "type": "characters" }
        }
    },
    "model": {
        "type": "crf_tagger_f1",
        #"label_encoding": "BIOUL",
        #"calculate_span_f1": true,
        "text_field_embedder": {
            "tokens": {
                "type": "embedding",
                "embedding_dim": word_embedding_dim
            },
            "token_characters": {
                "type": "character_encoding",
                "embedding": {
                    "embedding_dim": char_embedding_dim,
                },
                "encoder": {
                    "type": "lstm",
                    "input_size": char_embedding_dim,
                    "hidden_size": char_embedding_dim
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
            "type": "adam",
            "lr": learning_rate
        },
        "patience": patience
    }
}