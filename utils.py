"""
Utils file - argmin and argmax are taken from Peter Norvig's utils file
(http://www.norvig.com)

Author: Robert Berry
Date: 21st September 2011
"""

def count_if(pred, seq):
    """Returns a count of all the elements in seq matching the predicate.
    >>> count_if(lambda x: x % 2, range(0, 10))
    5
    """
    count = 0
    for x in seq:
        if pred(x): count += 1
    return count

def argmin(seq, fn):
    """Return an element with lowest fn(seq[i]) score; tie goes to first one.
    >>> argmin(['one', 'to', 'three'], len)
    'to'
    """
    best = seq[0]; best_score = fn(best)
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score
    return best

def argmax(seq, fn):
    """Return an element with highest fn(seq[i]) score; tie goes to first one.
    >>> argmax(['one', 'to', 'three'], len)
    'three'
    """
    return argmin(seq, lambda x: -fn(x))
