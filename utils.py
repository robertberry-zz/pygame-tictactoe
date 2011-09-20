



def count_if(pred, seq):
    count = 0
    for x in seq:
        if pred(x): count += 1
    return count
