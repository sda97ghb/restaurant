def grouped(iterable, key):
    """Like itertools.groupby(...) but groups together *all* items with the same key, not consecutive"""
    res = dict()
    for i in iterable:
        g = key(i)
        if g in res:
            res[g].append(i)
        else:
            res[g] = [i]
    return res
