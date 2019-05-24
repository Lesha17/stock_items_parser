import pandas as pd
from layers.utils.split_utils import separate_words_and_numbers, surround_with_spaces

df = pd.read_excel('temp/datasets/exists_ru/exists_ru_test.xlsx')
new_df = pd.DataFrame(columns=df.keys())

for index, row in df.iterrows():
    title = row['title_labeled']
    if not pd.isna(title):
        title = surround_with_spaces(title, '"', '"')
        title = surround_with_spaces(title, '-', '-')
        title = separate_words_and_numbers(title)
        title = title.replace('Наименование 1', 'Наименование1')
        new_row = row
        new_row['title_labeled'] = title
        new_df = new_df.append(new_row, ignore_index=True)

new_df.to_excel('temp/datasets/exists_ru/exists_ru_test_whitespaces.xlsx')
