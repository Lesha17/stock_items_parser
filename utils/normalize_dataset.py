from utils.dataset_normalizer import *
import utils.exists_ru.exists_ru_columns as exists_ru
import utils.krepmarket.krepmarket_columns as krepmarket

# Harcoded characteristics, so cannot use different dataset
# To use it, write own dataset normalizer

dn = DatasetNormalizer(krepmarket.TARGET_CHARACTERISTICS, krepmarket.ATTRIBUTES)
dn.normalize('datasets/krepmarket/krepmarket.xlsx', 'temp/datasets/krepmarket', 'krepmarket')

dn = DatasetNormalizer(exists_ru.CHARACTERISTICS, exists_ru.ATTRIBUTES)
dn.normalize('datasets/exists_ru/exists_ru.xlsx', 'temp/datasets/exists_ru', 'exists_ru')

