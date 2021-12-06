####################
#mutable and inmutable objects. Hashing function
####################
"""
Tuples with mutable items can be a source of bugs.
An object is only hashable if its value cannot ever change. An unhashable tuple cannot be inserted as a dict key, or a set element.

Comprobamos si es o no hashable, no podemos cambiar sus referencias, pero como alguna de las referencias sea mutable, entonces no es hashable
"""
def fixed(o):
    try:
        hash(o)
    except TypeError:
        return False
    return True

tf = (10, 'alpha', (1, 2))
tm = (10, 'alpha', [1, 2])
print(fixed(tf))
print(fixed(tm))
tm[-1].append(8)
print(tm)