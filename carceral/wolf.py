import os
import logging
import re
import sys

import wolframalpha

from carceral.slugify import slugify

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_client():
    return wolframalpha.Client(os.environ.get('WOLFRAM_API_ID'))


def get_wolfram_dictionary_multi_word(input):
    dictionary = []
    dictionary = get_wolfram_dictionary(input)
    if len(dictionary) == 0:
        words = input.split()
        for word in words:
            dictionary += get_wolfram_dictionary(word)
    return dictionary


def get_wolfram_dictionary(input):
    client = get_client()
    words = []
    try:
        res = client.query(input)
        for p in res.pods:
            if p.title == "Broader terms" or p.title == "Synonyms":
                for s in p.subpods:
                    _raw = s.plaintext.split('|')
                    words = [slugify(cleanse(s.strip())) for s in _raw]
                    logger.info(words)
    except Exception, e:
        logger.info(e)
        logger.info('could not get wolfram result for {0}'.format(input))

    return words


def cleanse(word):
    return re.sub("\(.*\)", '', word).strip()
