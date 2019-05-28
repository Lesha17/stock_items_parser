import re
from utils.dataset_normalizer import *

def prepare_stable(s):
    s = s.lower()
    s = replace_comma_in_numbers(s)
    return s

def prepare_value(s):
    s = prepare_stable(s)

    s = surround_with_spaces_numbers(s, 'x', 'x')
    s = surround_with_spaces_numbers(s, 'х', 'х')
    s = surround_with_spaces(s, '/', '/')
    s = surround_with_spaces_words(s, r'\.', '.')

    s = surround_with_spaces(s, ';', ';')
    s = surround_with_spaces(s, ',', ',')
    s = surround_with_spaces(s, r'\(', '(')
    s = surround_with_spaces(s, r'\)', ')')
    s = surround_with_spaces(s, r'\*', '*')
    s = surround_with_spaces(s, '-', '-')
    s = separate_words_and_numbers(s)

    return s


def split(s):
    tokens = re.split(r'\s|"', s)
    return [t for t in tokens if t is not None and t != '']

def prepare_and_split(s):
    return split(prepare_value(s))

def parse_prelabeled(s):
    find_from = 0

    parts = []
    tags = []

    first_tag_start_index = 0
    while first_tag_start_index != -1 and first_tag_start_index < len(s):
        first_tag_start_index = s.find('<', find_from)
        if first_tag_start_index != -1:
            first_tag_end_index = s.find('>', first_tag_start_index)
            tag_name = s[first_tag_start_index + 1:first_tag_end_index]
            second_tag_start_index = s.find('</', first_tag_end_index + 1)
            second_tag_end_index = s.find('>', second_tag_start_index)

            value = s[first_tag_end_index + 1:second_tag_start_index]

            before_tag = s[find_from:first_tag_start_index]
            if len(before_tag) > 0:
                parts.append(before_tag)
                tags.append('NONE_CHAR')

            if len(value) > 0:
                parts.append(value)
                tags.append(tag_name)

            find_from = second_tag_end_index + 1

    if find_from < len(s):
        parts.append(s[find_from:])
        tags.append('NONE_CHAR')

    return parts, tags

def split_and_get_tags(parts, parts_tags):
    tokens = []
    tags = []

    for i in range(len(parts)):
        part_tokens = split(prepare_value(parts[i]))
        tag = parts_tags[i]
        for t in part_tokens:
            tokens.append(t)
            tags.append(tag)

    return tokens, tags