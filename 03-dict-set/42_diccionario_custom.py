"""StrKeyDict always converts non-string keys to `str`

Test for initializer: keys are converted to `str`.

    >>> d = StrKeyDict([(2, 'two'), ('4', 'four')])
    >>> sorted(d.keys())
    ['2', '4']

Tests for item retrieval using `d[key]` notation::

    >>> d['2']
    'two'
    >>> d[4]
    'four'
    >>> d[1]
    Traceback (most recent call last):
      ...
    KeyError: '1'

Tests for item retrieval using `d.get(key)` notation::

    >>> d.get('2')
    'two'
    >>> d.get(4)
    'four'
    >>> d.get(1, 'N/A')
    'N/A'

Tests for the `in` operator::

    >>> 2 in d
    True
    >>> 1 in d
    False

Test for item assignment using non-string key::

    >>> d[0] = 'zero'
    >>> d['0']
    'zero'

Tests for update using a `dict` or a sequence of pairs::

    >>> d.update({6:'six', '8':'eight'})
    >>> sorted(d.keys())
    ['0', '2', '4', '6', '8']
    >>> d.update([(10, 'ten'), ('12', 'twelve')])
    >>> sorted(d.keys())
    ['0', '10', '12', '2', '4', '6', '8']
    >>> d.update([1, 3, 5])
    Traceback (most recent call last):
      ...
    TypeError: 'int' object is not iterable

"""
import collections


#Subclase de collections.UserDict
#Similar al otro ejemplo, pero haciendo el subclassing de UserDict tenemos que sobre-escribir menos métodos. UserDict no hereda de dict, la extiende usando "composition": hay un miembro en UserDict que se llama data que implementa un dict.
class StrKeyDict(collections.UserDict):  # <1>

    #Igual que antes. Este método es llamado por __getitems__ cuando la key no se encuentra en el diccionario, utilizando el operador []
    def __missing__(self, key):  # <2>
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    #Cuando ingresamos items en el diccionario nos aseguramos de que tanto si la key es str o int, se guarde como str
    def __setitem__(self, key, item):
        self.data[str(key)] = item  # <4>

    #La accion anterior nos permite simplificar la reescritura de __contains__
    def __contains__(self, key):
        return str(key) in self.data  # <3>


# END STRKEYDICT
