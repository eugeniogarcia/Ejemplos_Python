"""StrKeyDict0 converts non-string keys to `str` on lookup

# BEGIN STRKEYDICT0_TESTS

Tests for item retrieval using `d[key]` notation::

    >>> d = StrKeyDict0([('2', 'two'), ('4', 'four')])
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

# END STRKEYDICT0_TESTS
"""


#Subclase de dict
class StrKeyDict0(dict):

    # Implementamos __missing__, de modo que cuando hagamos un ["key"] y la "key" no exista, se ejecutará la lógica que incluyamos en este método
    def __missing__(self, key):
        #Si la key es de tipo string, se lanza un error
        if isinstance(key, str):
            raise KeyError(key)
        #en caso contrario, recuperamos la key stringificada
        return self[str(key)]

    #Reimplementamos el método get de dict
    def get(self, key, default=None):
        try:
            #Retorna el valor, o una excepcion si la key no existe - comportamiento por defecto de dict
            return self[key]
        except KeyError:
            #En caso de que la key no exista, retornamos el valor por defecto - que sera None sino indicamos otra cosa
            return default  # <5>

    #Reimplementamos in
    def __contains__(self, key):
        #Consideredamos que la key existe si esta presente bien tal cual - comportamiento por defecto de dict - o en formato string
        return key in self.keys() or str(key) in self.keys()  # <6>
