from collections import namedtuple
from a_coroutil import coroutine

Result = namedtuple('Result', 'count average')

@coroutine
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        if term is None:
            break  # <1>
        total += term
        count += 1
        average = total/count
    return Result(count, average)  # <2>
