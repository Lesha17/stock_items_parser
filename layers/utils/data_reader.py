import pandas as pd
import numpy as np
from typing import List, Dict, Iterator
from allennlp.data import DatasetReader, TokenIndexer, Token, Instance
from allennlp.data.fields import TextField, SequenceLabelField, ArrayField
from allennlp.data.token_indexers import SingleIdTokenIndexer

from layers.utils.split_utils import *

@DatasetReader.register('custom-dataset-reader')
class CustomDataReader(DatasetReader):
    def __init__(self, token_indexers: Dict[str, TokenIndexer] = None) -> None:
        super().__init__(lazy=True)
        self.token_indexers = token_indexers or {"tokens": SingleIdTokenIndexer()}

    def text_to_instance(self, tokens: List[Token], tags: List[str] = None) -> Instance:
        sentence_field = TextField(tokens, self.token_indexers)
        fields = {"tokens": sentence_field}

        if tags:
            label_field = SequenceLabelField(labels=tags, sequence_field=sentence_field)
            fields["tags"] = label_field

        return Instance(fields)

    def _read(self, file_path: str) -> Iterator[Instance]:
        df = pd.read_excel(file_path)
        for index, row in df.iterrows():
            if pd.isna(row['title_labeled']):
                continue

            parts, parts_tags = parse_prelabeled(str(row['title_labeled']))
            sentence, tags = split_and_get_tags(parts, parts_tags)

            yield self.text_to_instance([Token(w) for w in sentence], tags)
