from utils.dataset_normalizer import *
from utils.exists_ru.exists_ru_columns import CHARACTERISTICS, ATTRIBUTES

dn = DatasetNormalizer(CHARACTERISTICS, ATTRIBUTES)
dn.normalize('datasets/exists_ru/exists_ru.xlsx', 'temp/datasets/exists_ru', 'exists_ru')