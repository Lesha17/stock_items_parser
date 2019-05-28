'''

Given a dataset with title column, some valued characteristics columns,
some attribute columns and some junk columns (e.g. barcode, price, image link, etc.).
If there is title_prelabaled, it would be used

Purpose is to extract those values.

'''

import pandas as pd
import re

def replace_comma_in_numbers(s):
    return re.sub(r'(\d),(\d)', r'\1.\2', s)

def replace_dot_in_words(s):
    return re.sub(r'([^(\W|\d)] ?)\.( ?[^(\W|\d)])', r'\1 \2', s)

def replace_x_in_numbers(s, stable = True):
    if stable:
        return re.sub(r'(\d\s?)[xх](\s?\d)', r'\1*\2', s)
    else:
        return re.sub(r'(\d\s?)[xх](\s?\d)', r'\1 * \2', s)

def replace_slash_in_words(s):
    return re.sub(r'([^(\W|\d)] ?)/( ?[^(\W|\d)])', r'\1 \2', s)

def is_number_with_slash(s):
    return re.match(r'\d/\d', s) is not None

def replace_slash_in_numbers(s):
    return re.sub(r'(\d ?)/( ?\d)', r'\1 \2', s)

def surround_with_spaces(s, regex, char):
    s = re.sub(r'(\w\s?)' + regex, r'\1 ' + char, s)
    s = re.sub(regex + r'(\s?\w)', char + r' \1', s)
    return s

def surround_with_spaces_words(s, regex, char):
    return re.sub(r'([^(\W|\d)] ?)' + regex + r'( ?[^(\W|\d)])', r'\1 ' + char + r' \2', s)

def surround_with_spaces_numbers(s, regex, char):
    return re.sub(r'(\d\s?)' + regex + r'(\s?\d)', r'\1 ' + char + r' \2', s)

def separate_words_and_numbers(s):
    s = re.sub(r'([^(\W|\d)])(\d)', r'\1 \2', s)
    s = re.sub(r'(\d)([^(\W|\d)])', r'\1 \2', s)
    return s

def prepare_value(s):
    s = s.lower()
    s = replace_comma_in_numbers(s)
    s = replace_x_in_numbers(s)
    s = replace_slash_in_words(s)
    s = replace_slash_in_numbers(s)
    s = replace_dot_in_words(s)
    s = separate_words_and_numbers(s)
    return s

def prepare_stable(s):
    s = s.lower()
    s = replace_comma_in_numbers(s)
    s = replace_x_in_numbers(s)
    s = replace_slash_in_words(s)
    s = replace_slash_in_numbers(s)
    s = replace_dot_in_words(s)
    return s

def split(s):
    s = prepare_value(s)

    tokens = re.split(r'\s|\n|;|,|"|-|\*|\(|\)', s)
    return [t for t in tokens if t is not None and t != '']


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


def fill_title_intersects(title_intersects, start, end):
    title_intersects[start:end] = [True] * (end - start)


def fill(title_raw, char_name, start, end, positions, title_intersects, to_resolve = None, to_resolve_df = pd.DataFrame(),
         original_value = ''):
    if start and end:
        if char_name not in positions:
            positions[char_name] = []
        positions[char_name].append((start, end))
        fill_title_intersects(title_intersects, start, end)
    elif to_resolve:
        for start, end in to_resolve:
            to_resolve_df = to_resolve_df.append({'title': title_raw, 'char_name': char_name,
                                                  'char_value': title_raw[start:end], 'original_value': original_value},
                                                 ignore_index=True)

    return to_resolve_df


def parse_prelabeled_and_apply(title_prelabeled, positions, title_intersects):
    char_to_indices = parse_prelabeled(title_prelabeled)
    for char_name, (start, end) in char_to_indices.items():
        fill(title_prelabeled, char_name, start, end, positions, title_intersects)


def get_title_token_positions(title, title_tokens):
    result = []
    find_from = 0
    for t in title_tokens:
        index = title.find(t, find_from)
        result.append(index)
        find_from = index + len(t)
    return result

def extract_char_positions(title_raw, char_value,
                           step, max_step, title_intersects):
    extracted_char_positions = []

    title_tokens = split(title_raw)
    title_token_positions = get_title_token_positions(prepare_stable(title_raw), title_tokens)

    char_value_tokens = split(char_value)

    for i in range(len(title_tokens)):
        extracted_token_indices = []
        # Findings matching tokens sequence
        for j in range(len(char_value_tokens)):
            index = i + j
            if index >= len(title_tokens):
                break
            title_token = title_tokens[index]
            char_value_token = char_value_tokens[j]
            if char_value_token == title_token \
                    or char_value_token.startswith(title_token) \
                    or (len(title_token) >= 3 and title_token.startswith(char_value_token)) \
                    or (step > 1 and title_token.startswith(char_value_token)) \
                    or (step > 2 and title_token[:3] == char_value_token[:3]):
                extracted_token_indices.append(index)
            elif step < 2:
                break

        # Append match
        if len(extracted_token_indices) > 0:
            first = extracted_token_indices[0]
            last = extracted_token_indices[-1]

            start = title_token_positions[first]
            end = title_token_positions[last] + len(title_tokens[last])
            if not any(title_intersects[start:end]): # Must not intersects with already extracted chars
                extracted_char_positions.append((start, end, len(extracted_token_indices)))

    if len(extracted_char_positions) > 0:
        max_tokens_count = max(arr[2] for arr in extracted_char_positions)
        extracted_char_positions = [(start, end) for start, end, tokens_num in extracted_char_positions
                                    if tokens_num >= max_tokens_count]

        if (max_tokens_count == 1 and step > 0) or step > 1:
            extracted_char_positions = [max(extracted_char_positions, key=lambda tupl: tupl[1] - tupl[0])]

        if len(extracted_char_positions) == 1:
            start = extracted_char_positions[0][0]
            end = extracted_char_positions[0][1]

            return start, end, None

        elif step == max_step:
            return None, None, extracted_char_positions

    return None, None, None


def get_char_value_if_need_extracting(row, char_name, original_char_name, extracted_chars):
    if char_name in extracted_chars:
        return None
    if pd.isna(row[original_char_name]):
        return None
    char_value = str(row[original_char_name])
    if not char_value or char_value == '':
        return None
    return char_value



def get_labeled_tittle(title_raw, positions):
    p2c = []
    for c, pos in positions.items():
        for start, end in pos:
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

class DatasetNormalizer:
    def __init__(self, characteristics, attributes, attr_yes_values = ['да', 'есть']):
        print(characteristics)
        print(attributes)
        self.characteristics = characteristics
        self.attributes = attributes
        self.attr_yes_values = attr_yes_values
        self.all_chars = {}
        self.columns = []
        for char_name, originals in self.characteristics.items():
            for original_char_name in originals:
                self.all_chars[original_char_name] = char_name
            self.columns.append(char_name)
        for char_name in self.attributes:
            self.all_chars[char_name] = char_name
            self.columns.append(char_name)

    def normalize(self, input_file, output_dir, dataset_name):

        df = pd.read_excel(input_file)
        result_df = pd.DataFrame(columns=['title', 'title_labeled'] + self.columns)
        to_resolve_df = pd.DataFrame(columns=['title', 'char_name', 'char_value'])

        for index, row in df.iterrows():
            title_raw = str(row['title'])
            title_intersects = [False] * len(title_raw)

            result_row = {}
            result_row['title'] = title_raw

            positions = {}

            if not pd.isna(row['title_prelabeled']):
                parse_prelabeled_and_apply(str(row['title_prelabeled']), positions, title_intersects)

            max_step = 3
            for step in range(max_step + 1):
                for char_name, originals in self.characteristics.items():
                    for original_char_name in originals:
                        char_value = get_char_value_if_need_extracting(row, char_name, original_char_name, positions)
                        if char_value:
                            start, end, to_resolve = extract_char_positions(title_raw, char_value, step, max_step, title_intersects)
                            to_resolve_df = fill(title_raw, char_name, start, end, positions, title_intersects, to_resolve,
                                             to_resolve_df, char_value)

                for char_name in self.attributes:
                    char_value = get_char_value_if_need_extracting(row, char_name, char_name, positions)
                    if char_value:
                        if char_value.lower() in self.attr_yes_values:
                            start, end, to_resolve = extract_char_positions(title_raw, char_name, step, max_step, title_intersects)
                            to_resolve_df = fill(title_raw, char_name, start, end, positions, title_intersects, to_resolve,
                                                 to_resolve_df, char_name)

            for original_char_name, char_name in self.all_chars.items():
                if not pd.isna(row[original_char_name]):
                    result_row[char_name] = row[original_char_name]

            result_row['title_labeled'] = get_labeled_tittle(title_raw, positions)
            result_df = result_df.append(result_row, ignore_index=True)

            for original_char_name, char_name in self.all_chars.items():
                if char_name in positions:
                    continue
                char_value = get_char_value_if_need_extracting(row, char_name, original_char_name, positions)
                if char_value and char_name not in positions:
                    to_resolve_df = to_resolve_df.append({'title': title_raw, 'char_name': char_name,
                                                          'char_value': None,
                                                          'original_value': char_value},
                                                         ignore_index=True)


            if index % 100 == 0:
                print('Processed {0} out of {1} ({2:.2f} %)'.format(index, len(df.index),
                                                                    (100 * (index / len(df.index)))))

        result_df.to_excel(output_dir + '/' + dataset_name + '_normalized.xlsx')
        to_resolve_df.to_excel(output_dir + '/' + dataset_name + '_to_resolve.xlsx')




