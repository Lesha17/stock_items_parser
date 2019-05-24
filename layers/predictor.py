from layers.utils.splitter import CustomWordSplitter

from allennlp.predictors import Predictor
from allennlp.predictors import SentenceTaggerPredictor


@Predictor.register('custom-predictor')
class CustomPredictor(SentenceTaggerPredictor):
    def __init__(self, model, dataset_reader):
        super(CustomPredictor, self).__init__(model, dataset_reader)
        self._tokenizer = CustomWordSplitter()

