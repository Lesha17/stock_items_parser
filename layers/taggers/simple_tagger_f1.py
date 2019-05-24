
from typing import Dict, Optional, List, Any

import numpy
from allennlp.models import SimpleTagger
from overrides import overrides
import torch
from torch.nn.modules.linear import Linear
import torch.nn.functional as F

from allennlp.common.checks import check_dimensions_match, ConfigurationError
from allennlp.data import Vocabulary
from allennlp.modules import Seq2SeqEncoder, TimeDistributed, TextFieldEmbedder
from allennlp.models.model import Model
from allennlp.nn import InitializerApplicator, RegularizerApplicator

import layers.utils.f1_support as f1_support

@Model.register("simple_tagger_f1")
class SimpleTaggerF1(SimpleTagger):
    def __init__(self, vocab: Vocabulary,
                 text_field_embedder: TextFieldEmbedder,
                 encoder: Seq2SeqEncoder,
                 initializer: InitializerApplicator = InitializerApplicator(),
                 regularizer: Optional[RegularizerApplicator] = None,
                 verbose_metrics = False) -> None:
        super().__init__(vocab, text_field_embedder, encoder, initializer, regularizer)

        self._verbose_metrics = verbose_metrics
        f1_support.add_f1(self)

    def get_metrics(self, reset: bool = False):
        return f1_support.get_metrics(self, reset)
