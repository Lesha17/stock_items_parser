from typing import Dict, Optional, List, Any

from allennlp.data import Vocabulary
from allennlp.models import CrfTagger
from allennlp.modules import TextFieldEmbedder
from allennlp.common.checks import check_dimensions_match, ConfigurationError
from allennlp.data import Vocabulary
from allennlp.modules import Seq2SeqEncoder, TimeDistributed, TextFieldEmbedder
from allennlp.modules import ConditionalRandomField, FeedForward
from allennlp.modules.conditional_random_field import allowed_transitions
from allennlp.models.model import Model
from allennlp.nn import InitializerApplicator, RegularizerApplicator
import allennlp.nn.util as util
from allennlp.training.metrics import CategoricalAccuracy, SpanBasedF1Measure, F1Measure


@Model.register("crf_tagger_f1")
class CrfTaggerWithMetric(CrfTagger):
    def __init__(self, vocab: Vocabulary,
                 text_field_embedder: TextFieldEmbedder,
                 encoder: Seq2SeqEncoder,
                 label_namespace: str = "labels",
                 feedforward: Optional[FeedForward] = None,
                 label_encoding: Optional[str] = None,
                 include_start_end_transitions: bool = True,
                 constrain_crf_decoding: bool = None,
                 calculate_span_f1: bool = None,
                 dropout: Optional[float] = None,
                 verbose_metrics: bool = False,
                 initializer: InitializerApplicator = InitializerApplicator(),
                 regularizer: Optional[RegularizerApplicator] = None) -> None:
        super().__init__(vocab,
                         text_field_embedder,
                         encoder,
                         label_namespace,
                         feedforward,
                         label_encoding,
                         include_start_end_transitions,
                         constrain_crf_decoding,
                         calculate_span_f1,
                         dropout,
                         verbose_metrics,
                         initializer,
                         regularizer)
        for label, index in self.vocab.get_token_to_index_vocabulary('labels').items():
            self.metrics["f1_" + label.replace(' ', '_')] = F1Measure(index)

    def get_metrics(self, reset: bool = False):
        result = {}
        f1_sum = 0
        f1_count = 0
        for name, metric in self.metrics.items():
            if name.startswith("f1"):
                # With only true_negatives it could be 0 and break a metric
                if metric._true_positives + metric._false_positives + metric._false_negatives > 0:
                    precision, recall, f1_measure = metric.get_metric(reset=reset)
                    f1_sum += f1_measure
                    f1_count += 1
            else:
                result[name] = metric.get_metric(reset=reset)
        if f1_count > 0:
            result['f1_total'] = f1_sum / f1_count

        return result

