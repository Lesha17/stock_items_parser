from allennlp.common import Params
from allennlp.data import DatasetReader
from allennlp.models import Archive, CrfTagger, Model
from allennlp.predictors import SentenceTaggerPredictor, Predictor

from layers.utils.data_reader import CustomDataReader
from layers.utils.splitter import CustomWordSplitter
from utils.dataset_normalizer import parse_prelabeled
import pandas as pd
import numpy as np
from utils.dataset_normalizer import get_title_token_positions
from utils.dataset_normalizer import get_labeled_tittle
from layers.utils.split_utils import prepare_and_split
from layers.utils.split_utils import prepare_stable
from utils.exists_ru.exists_ru_columns import CHARACTERISTICS, ATTRIBUTES
from layers.taggers import *
from layers.taggers.crf_with_f1 import *

params = Params.from_file('models/crf_lstm_characters_only.jsonnet')
model = Model.load(params, 'output/models/crf_lstm_characters_only_additional_split/exists_ru')

reader_params = params.pop('dataset_reader')
reader_type = reader_params.pop('type')
reader = DatasetReader.by_name(reader_type).from_params(reader_params)

predictor = SentenceTaggerPredictor(model, dataset_reader = reader)
predictor._tokenizer = CustomWordSplitter()

def get_tags(title):
    tokens = prepare_and_split(title)

    tag_logits = predictor.predict(title)['logits']
    tag_ids = np.argmax(tag_logits, axis=-1)
    tags = [model.vocab.get_token_from_index(i, 'labels') for i in tag_ids]

    return tokens, tags
