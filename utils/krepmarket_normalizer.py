import pandas as pd
import re

df = pd.read_excel('datasets/krepmarket.xlsx')

def replace_comma_in_numbers(s):
    return re.sub(r'(\d),(\d)', r'\1.\2', s)

def replace_dot_in_words(s):
    return re.sub(r'([^(\W|\d)] ?)\.( ?[^(\W|\d)])', r'\1 \2', s)

print(replace_comma_in_numbers('22,18'))
print(replace_dot_in_words('22.18'))
print(replace_dot_in_words('дер .полн'))

def replace_x_in_numbers(s):
    return re.sub(r'(\d ?)[xх]( ?\d)', r'\1*\2', s)

replace_x_in_numbers('22 x18')

def replace_slash_in_words(s):
    return re.sub(r'([^(\W|\d)] ?)/( ?[^(\W|\d)])', r'\1 \2', s)

def is_number_with_slash(s):
    return re.match(r'\d/\d', s) is not None

def replace_slash_in_numbers(s):
    return re.sub(r'(\d ?)/( ?\d)', r'\1 \2', s)

def surround_with_spaces(s, regex, char):
    return re.sub(r'(\w ?)' + regex + '( ?\w)', r'\1 ' + char + r' \2', s)

def surround_with_spaces_words(s, regex, char):
    return re.sub(r'([^(\W|\d)] ?)' + regex + '( ?[^(\W|\d)])', r'\1 ' + char + r' \2', s)

def split(s):
    tokens = re.split(' |\n|;|,|\\*', s)
    return [t for t in tokens if t is not None and t != '']

def prepare_value(s):
    s = s.lower()
    s = replace_comma_in_numbers(s)
    s = replace_x_in_numbers(s)
    s = replace_slash_in_words(s)
    s = replace_slash_in_numbers(s)
    s = replace_dot_in_words(s)
    return s

def parse_prelabeled(s):
    find_from = 0
    original_s = ''

    result = {}

    first_tag_start_index = 0
    while first_tag_start_index != -1 and first_tag_start_index < len(s):
        first_tag_start_index = s.find('<', find_from)
        if first_tag_start_index != -1:
            first_tag_end_index = s.find('>', first_tag_start_index)
            tag_name = s[first_tag_start_index+1:first_tag_end_index]
            second_tag_start_index = s.find('</', first_tag_end_index+1)
            second_tag_end_index = s.find('>', second_tag_start_index)

            value = s[first_tag_end_index+1:second_tag_start_index]

            original_s += s[find_from:first_tag_start_index]
            value_start_index = len(original_s)
            original_s += value
            value_end_index = len(original_s)

            result[tag_name] = (value_start_index, value_end_index)
            find_from = second_tag_end_index + 1

    return result

MATERIAL = ['Материал', 'Материал рукоятки']

TYPE = ['Тип', 'Тип головки', 'Резьба', 'Наконечник', 'Тип Заклепки', 'Тип анкера', 'Тип болта', 'Тип Шплинта',
        'В комплекте', 'Форма', 'Вид декорации', 'Вид зажима', 'Тип цепи', 'Звено', 'Тип крепления',
        'Размер']  # M / L

TYPE_ATTRIBUTES = ['С наружными зубцами', 'Для бетона', 'Универсальный', 'Левая резьба',
                   'Серьга', 'Набор', 'Мелкий шаг резьбы', 'Клипса', 'Изоляции',
                   'Дюймовый крепеж', 'Со скобой', 'Оборудование', 'Высокопрочные',
                   'Хомут-стяжка', 'Антивандальные', 'Внутренняя резьба', 'Бортик',
                   'Для высоких нагрузок', 'Держатель труб', 'Насечка', 'Соединитель цепи',
                   'Устойчивость к УФ', 'С предохраняющей гайкой', 'Спиральная',
                   'Карабин', 'Асимметричный', 'С коушем', 'Открытый',
                   'С роликом', 'Защита от перегрева', 'Регулируемая скорость',
                   'Регулировка глубины строгания', 'Выборка четверти', 'Насадки в комплекте',
                   'Сменные сопла', 'Регулируемая температура', 'Клинья для молотка', 'Трещотка',
                   ]  # Yes / No values

MODEL = ['Модель', 'Стандарт', 'Бита', 'Тип скоб']

COLOR = ['Цвет', 'Полоса']

SIZE1 = ['Длина, мм', 'Длина', 'Высота', 'Длина, м', 'Длина шины, см', 'Минимальный размер, мм',
         'Посадочный квадрат', 'Максимальный захват, мм', 'Размер скобы', 'Размер, мм']

SIZE2 = ['Диаметр, мм', 'Диаметр резьбы, мм', 'Диаметр резьбы, М', 'Диаметр',
         'Минимальный диаметр, мм', 'Максимальный диаметр, мм', 'Диаметр стержня, мм',
         'Глубина строгания, мм', 'Глубина выборки четверти, макс, мм',
         'Максимальная рабочая высота', 'Высота в сложенном состоянии',
         'Ширина', 'Ширина, мм', 'Размер гайки, М', 'Ширина ножа, мм',
         'Максимальный Размер, мм', 'Ширина режущей части, мм']

WEIGHT = ['Вес', 'Объем']
PHYS = ['Грузоподъемность', 'Мощность', 'Число оборотов, макс', 'Рабочая температура, макс, град.',
        'Расход воздуха, л/мин', 'Обороты, макс', 'Производительность, г/мин', 'Время нагрева, мин',
        'Максимальное усилие, Нм', 'Max рабочая нагрузка, кг', 'Максимальная нагрузка',
        'Грузоподъёмность на 1 единицу, кг', 'Грузоподъёмность на пару, кг', 'Допустимый пусковой ток, А',
        ]

COUNT = ['Количество', 'Количество звеньев цепи', 'Количество ступеней', 'Количество ступеней в секции',
         'Количество секций', 'Количество клавиш']

SUPPLIER = ['Производитель']
SUPPLIER_COUNTRY = ['Страна производитель']

PURPOSE = ['Применение']
DESTINATION = ['Назначение']

TARGET_CHARACTERISTICS = {
    'MATERIAL': MATERIAL,
    'TYPE': TYPE,
    'MODEL': MODEL,
    'COLOR': COLOR,
    'SIZE1': SIZE1,
    'SIZE2': SIZE2,
    'WEIGHT': WEIGHT,
    'PHYS': PHYS,
    'COUNT': COUNT,
    'SUPPLIER': SUPPLIER,
    'SUPPLIER_COUNTRY': SUPPLIER_COUNTRY,
    'PURPOSE': PURPOSE,
    'DESTINATION': DESTINATION
}

CHARACTERISTICS = ['Материал', 'Материал рукоятки',
                   'Тип', 'Тип головки', 'Резьба', 'Наконечник', 'Тип Заклепки', 'Тип анкера', 'Тип болта',
                   'Тип Шплинта',
                   'В комплекте', 'Форма', 'Вид декорации', 'Вид зажима', 'Тип цепи', 'Звено', 'Тип крепления',
                   'Размер',
                   'Модель', 'Стандарт', 'Бита', 'Тип скоб',
                   'Цвет', 'Полоса',
                   'Длина, мм', 'Длина', 'Высота', 'Длина, м', 'Длина шины, см', 'Минимальный размер, мм',
                    'Посадочный квадрат', 'Максимальный захват, мм', 'Размер скобы', 'Размер, мм',
                    'Диаметр, мм', 'Диаметр резьбы, мм', 'Диаметр резьбы, М', 'Диаметр',
                    'Минимальный диаметр, мм', 'Максимальный диаметр, мм', 'Диаметр стержня, мм',
                    'Глубина строгания, мм', 'Глубина выборки четверти, макс, мм',
                    'Максимальная рабочая высота', 'Высота в сложенном состоянии',
                    'Ширина', 'Ширина, мм', 'Размер гайки, М', 'Ширина ножа, мм',
                    'Максимальный Размер, мм', 'Ширина режущей части, мм',
                   'Вес', 'Объем',
        'Грузоподъемность', 'Мощность', 'Число оборотов, макс', 'Рабочая температура, макс, град.',
        'Расход воздуха, л/мин', 'Обороты, макс', 'Производительность, г/мин', 'Время нагрева, мин',
        'Максимальное усилие, Нм', 'Max рабочая нагрузка, кг', 'Максимальная нагрузка',
        'Грузоподъёмность на 1 единицу, кг', 'Грузоподъёмность на пару, кг', 'Допустимый пусковой ток, А',
        'Количество', 'Количество звеньев цепи', 'Количество ступеней', 'Количество ступеней в секции',
         'Количество секций', 'Количество клавиш',
        'Производитель', 'Страна производитель', 'Применение', 'Назначение']

ATTRIBUTES = ['С наружными зубцами', 'Для бетона', 'Универсальный', 'Левая резьба',
                   'Серьга', 'Набор', 'Мелкий шаг резьбы', 'Клипса', 'Изоляции',
                   'Дюймовый крепеж', 'Со скобой', 'Оборудование', 'Высокопрочные',
                   'Хомут-стяжка', 'Антивандальные', 'Внутренняя резьба', 'Бортик',
                   'Для высоких нагрузок', 'Держатель труб', 'Насечка', 'Соединитель цепи',
                   'Устойчивость к УФ', 'С предохраняющей гайкой', 'Спиральная',
                   'Карабин', 'Асимметричный', 'С коушем', 'Открытый',
                   'С роликом', 'Защита от перегрева', 'Регулируемая скорость',
                   'Регулировка глубины строгания', 'Выборка четверти', 'Насадки в комплекте',
                   'Сменные сопла', 'Регулируемая температура', 'Клинья для молотка', 'Трещотка']

YES_VALUES = ['да']

NONE_CHAR = 'NONE_CHAR'

CHAR_NAME_TO_CHAR = {}

for char, char_names in TARGET_CHARACTERISTICS.items():
    for char_name in char_names:
        CHAR_NAME_TO_CHAR[char_name] = char

def result_cols():
    result_cols = ['title', 'title_labeled']
    for char in TARGET_CHARACTERISTICS:
        result_cols.append(char)
    result_cols.append('ATTRIBUTES')
    return result_cols

print(result_cols())

def parse_prelabeled_and_apply(title_prelabeled):
    char_to_indices = parse_prelabeled(title_prelabeled)
    for char_name, (start, end) in char_to_indices.items():
        char = CHAR_NAME_TO_CHAR[char_name]
        positions_all_names[char_name] = [(start, end)]
        if char not in positions:
            positions[char] = []
        positions[char].append((start, end))

def extract_char_positions(char, char_name, char_value):
    if char_name in positions_all_names and len(positions_all_names[char_name]) > 0:
        return

    extracted_char_positions = []

    if char_name not in result_row_all_char:
        char_value_in_result = ''
        if char in result_row:
            char_value_in_result = result_row[char] + ', '
        result_row[char] = char_value_in_result + char_value
        result_row_all_char[char_name] = char_value

    title = prepare_value(title_raw)
    title_tokens = split(title)

    title_token_positions = []
    find_from = 0
    for t in title_tokens:
        index = title.find(t, find_from)
        title_token_positions.append(index)
        find_from = index + len(t)

    if title == prepare_value('Саморез по дереву PH 3,5 х25 полная п/сф оцинк MUS'):
        print(title_tokens, title_token_positions)

    char_value_tokens = split(char_value)

    for i in range(len(title_tokens)):
        extracted_token_indices = []
        for j in range(len(char_value_tokens)):
            index = i + j
            if index >= len(title_tokens):
                break
            title_token = title_tokens[index]
            char_value_token = char_value_tokens[j]
            if char_value_token.startswith(title_token) or (
                    step > 1 and title_token.startswith(char_value_token)
            ) or (
                step > 2 and title_token[:3] == char_value_token[:3]
            ):
                extracted_token_indices.append(index)
            elif step < 2:
                break

        if len(extracted_token_indices) > 0:
            first = extracted_token_indices[0]
            last = extracted_token_indices[-1]

            start = title_token_positions[first]
            end = title_token_positions[last] + len(title_tokens[last])
            if not any(title_intersects[start:end]):
                extracted_char_positions.append([start, end, len(extracted_token_indices)])

                if title == prepare_value('Саморез по дереву PH 3,5 х25 полная п/сф оцинк MUS') and char == 'TYPE':
                    print(char_name, char_value, start, end)
                    print([title_tokens[i] for i in extracted_token_indices])

    if len(extracted_char_positions) > 0:
        max_tokens_count = max(arr[2] for arr in extracted_char_positions)
        extracted_char_positions = [arr for arr in extracted_char_positions if arr[2] >= max_tokens_count]

        if max_tokens_count == 1 and step > 0:
            extracted_char_positions = [max(extracted_char_positions, key=lambda arr: arr[1] - arr[0])]

        if len(extracted_char_positions) == 1:
            start = extracted_char_positions[0][0]
            end = extracted_char_positions[0][1]

            if title == prepare_value('Саморез по дереву PH 3,5 х25 полная п/сф оцинк MUS') and char == 'TYPE':
                print('Selected: ' + title[start:end])

            title_intersects[start:end] = [True] * (end - start)

            if char not in positions:
                positions[char] = []
            positions[char].append((start, end))

            if char_name not in positions_all_names:
                positions_all_names[char_name] = [];
            positions_all_names[char_name].append((start, end));

        '''elif step > 0:
            for start_end in extracted_char_positions:
                to_resolve = to_resolve.append({'title': title, 'char_name': char, 'char_value': char_value,
                                                'extracted_char_value': title[start_end[0]:start_end[1]],
                                                'value_start': start_end[0]},
                                               ignore_index=True)
                                               '''
    if title == prepare_value('Саморез по дереву PH 3,5 х25 полная п/сф оцинк MUS'):
        for char, pos in positions.items():
            for start, end in pos:
                print('{}: {}, {}, {}'.format(char, title[start:end], start, end))


def get_labeled_tittle(positions):
    p2c = []
    for c, ps in positions.items():
        for start, end in ps:
            p2c.append((start, end, c))

    prev_index = 0
    title_labeled_tokens = []
    p2c.sort(key = lambda sec: sec[0])
    for start, end, c in p2c:
        if start - prev_index > 0:
            title_labeled_tokens.append(title_raw[prev_index:start])
        title_labeled_tokens.append('<{}>{}</{}>'.format(c, title_raw[start:end], c))
        prev_index = end
    if prev_index < len(title_raw):
        title_labeled_tokens.append(title_raw[prev_index:])

    return ''.join(title_labeled_tokens)

result_df = pd.DataFrame(columns=result_cols())
result_df_allnames = pd.DataFrame()

to_resolve = pd.DataFrame(columns=['title', 'char_name', 'char_value', 'extracted_char_value', 'value_start'])
for index, row in df.iterrows():
    title_raw = str(row['Название'])
    title_intersects = [False] * len(title_raw)

    result_row = {}
    result_row['title'] = title_raw

    result_row_all_char = {}
    result_row_all_char['title'] = title_raw

    positions = {}
    positions_all_names = {}

    if not pd.isna(row['title_prelabeled']):
        parse_prelabeled_and_apply(str(row['title_prelabeled']))

    for step in range(4):
        for char, char_names in TARGET_CHARACTERISTICS.items():
            for char_name in char_names:
                if pd.isna(row[char_name]):
                    continue
                char_value = prepare_value(str(row[char_name]))
                if not char_value or char_value == '':
                    print('Char value is none')
                    continue

                extract_char_positions(char, char_name, char_value)

        char = 'ATTRIBUTES'
        for char_name in TYPE_ATTRIBUTES:
            if str(row[char_name]).lower() in YES_VALUES:
                extract_char_positions(char, char_name, prepare_value(char_name))


    result_row['title_labeled'] = get_labeled_tittle(positions)
    result_df = result_df.append(result_row, ignore_index=True)

    result_row_all_char['title_labeled'] = get_labeled_tittle(positions_all_names)
    result_df_allnames = result_df_allnames.append(result_row_all_char, ignore_index=True)

    if index % 100 == 0:
        print('Processed {0} out of {1} ({2:.2f} %)'.format(index, len(df.index), (100 * (index / len(df.index)))))

to_resolve.to_excel('datasets/krepmarket_to_resolve.xlsx')
result_df.to_excel('datasets/krepmarket_merged.xlsx')
result_df_allnames.to_excel('datasets/krepmarket_all_chars.xlsx')