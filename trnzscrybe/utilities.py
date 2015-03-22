"""Utilities."""

import operator


def dec_2_b(dec, base):
    """Convert decimal to irregular number base system."""
    
    num = []
    for bi in base:
        num += [dec/(bi)]
        dec = dec%(bi)
        
    return num

def combinations(list_of_lists, verbose=False):
    """Generate all combinations."""

    lens = [len(x) for x in list_of_lists]
    total = reduce(operator.mul, lens)
    base = (lens+[1])[1:]
    base = [reduce(operator.mul, base[i:]) for i in range(len(base))]

    if verbose:
        print 'total {0}'.format(total)
        print 'base {0}'.format(base)

    return [[list_of_lists[i][elem] for i,elem in enumerate(dec_2_b(i, base))] for i in range(total)]
