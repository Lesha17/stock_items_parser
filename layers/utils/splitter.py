from typing import List
from allennlp.data.tokenizers.word_splitter import WordSplitter
from allennlp.data.tokenizers.token import Token

from layers.utils.split_utils import *


@WordSplitter.register('custom-word-splitter')
class CustomWordSplitter(WordSplitter):
    def split_words(self, sentence: str) -> List[Token]:
        return [Token(w) for w in split(prepare_value(sentence))]
