import pandas as pd
import numpy as np

prefix = 'temp/datasets/exists_ru/exists_ru'

df = pd.read_excel(prefix + '_normalized.xlsx')

msk = np.random.rand(len(df)) < 0.1

train = df[msk]
other = df[~msk]

msk_test = np.random.rand(len(other)) < 0.05
test = other[msk_test]

train.to_excel(prefix + '_train.xlsx')
test.to_excel(prefix + '_test.xlsx')
other.to_excel(prefix + '_other.xlsx')