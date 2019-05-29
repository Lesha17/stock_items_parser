from allennlp.data import Vocabulary
from allennlp.data.fields import SequenceLabelField
from typing import Dict, List, Union, Set, Iterator
from allennlp.data.fields.sequence_field import SequenceField


class CustomSequenceLabelField(SequenceLabelField):
    def __init__(self,
                 labels: Union[List[str], List[int]],
                 sequence_field: SequenceField,
                 label_namespace: str = 'labels') -> None:
        super().__init__(labels, sequence_field, label_namespace)

    def index(self, vocab: Vocabulary):
        if self._indexed_labels is None:
            self._indexed_labels = [self.get_token_index_in_vocab(vocab, label)  # type: ignore
                                    for label in self.labels]

    def get_token_index_in_vocab(self, vocab, label):
        try:
            return vocab.get_token_index(label, self._label_namespace)
        except KeyError:
            return vocab.get_token_index('NONE_CHAR', self._label_namespace)
