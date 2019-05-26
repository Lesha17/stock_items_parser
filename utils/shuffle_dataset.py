import pandas as pd

dataset = 'temp/datasets/exists_ru/exists_ru_train.xlsx'
df = pd.read_excel(dataset)
df = df.sample(frac=1).reset_index(drop=True)
df.to_excel(dataset)