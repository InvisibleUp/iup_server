import functools
import operator

# https://stackoverflow.com/a/1469274/
def subdict_from_key_list(d, l, subkey=None):
    return functools.reduce(operator.getitem, l, d)
