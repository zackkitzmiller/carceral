import re


def slugify(text, separator="-"):
    ret = text
    ret = re.sub("([a-zA-Z])(uml|acute|grave|circ|tilde|cedil)", r"\1", ret)
    ret = re.sub("\W", " ", ret)
    ret = ret.strip()
    ret = re.sub(" +", separator, ret)
    return ret.strip()
