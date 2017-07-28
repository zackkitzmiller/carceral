import os
import random
import re

fileDir = os.path.dirname(os.path.realpath('__file__'))
filename = os.path.join(fileDir, 'dat/words')
filename = os.path.abspath(os.path.realpath(filename))
WORDS = open(filename).read().splitlines()


def slugify(text, separator="-"):
    ret = text
    ret = re.sub("([a-zA-Z])(uml|acute|grave|circ|tilde|cedil)", r"\1", ret)
    ret = re.sub("\W", " ", ret)
    ret = ret.strip()
    ret = re.sub(" +", separator, ret)
    return ret.strip()


def get_words_from_dictionary(dictionary, num_words=1):
    words = []
    for i in xrange(0, num_words):
        words.append(random.choice(dictionary).lower())
    return "-".join(words)


def get_standard_dictionary():
    return WORDS
