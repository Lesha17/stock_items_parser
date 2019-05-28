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