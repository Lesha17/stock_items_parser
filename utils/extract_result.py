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

params = Params.from_file('models/crf_lstm_with_characters.jsonnet')
model = Model.load(params, 'output/models/crf_lstm_with_characters/exists_ru')

reader_params = params.pop('dataset_reader')
reader_type = reader_params.pop('type')
reader = DatasetReader.by_name(reader_type).from_params(reader_params)

predictor = SentenceTaggerPredictor(model, dataset_reader = reader)
predictor._tokenizer = CustomWordSplitter()

test_df = pd.read_excel('temp/datasets/exists_ru/exists_ru_test.xlsx')

parsing_result_df = pd.DataFrame(columns=['title', 'title_labeled_correct', 'title_labeled'] + CHARACTERISTICS + ATTRIBUTES)
for index, row in test_df.iterrows():
    title = str(row['title'])
    title_labeled_correct = str(row['title_labeled'])
    result_row = {'title': title, 'title_labeled_correct': title_labeled_correct}

    tokens = prepare_and_split(title)
    token_positions = get_title_token_positions(prepare_stable(title), tokens)

    tag_logits = predictor.predict(title)['logits']
    tag_ids = np.argmax(tag_logits, axis=-1)
    tags = [model.vocab.get_token_from_index(i, 'labels') for i in tag_ids]

    positions = {}
    for i in range(len(tags)):
        tag = tags[i]
        if tag != 'NONE_CHAR':
            if tag not in positions:
                positions[tag] = []
            positions[tag].append((token_positions[i], token_positions[i] + len(tokens[i])))
            if tag not in result_row:
                result_row[tag] = ''
            result_row[tag] += ' ' + tokens[i]

    title_labeled = get_labeled_tittle(title, positions)
    result_row['title_labeled'] = title_labeled

    parsing_result_df = parsing_result_df.append(result_row, ignore_index=True)

parsing_result_df.to_excel('temp/datasets/exists_ru/exists_ru_result.xlsx')