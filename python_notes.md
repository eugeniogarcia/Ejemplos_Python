- [Comprenhension](#comprenhension)
- [Generadores](#gen)
- [Colas](#colas)
- [Pattern Matching](#patron)
- [Copia de objetos. Shallow y Deep Copy](#copia)
- [Métodos especiales](#esp)
- [Diccionarios](#dicc)
- [Sets](#set)
- [Crear clases](#clases)
- [Programacion funcional](#func)
- [Tipificación de objetos](#hint)
- [Decoradores](#dec)
- [Caso práctico de Modelado de Objetos](#modelado)
- [Clases Abstractas](#ABC)
- [Protocolos](#protocol)

# Varios

## <a name="comprenhension">Comprehension</a>

Son equivalentes:

```py
beyond_ascii = [ord(s) for s in symbols if ord(s) > 127]

beyond_ascii = list(filter(lambda c: c > 127, map(ord, symbols)))
```

Producto cartesiano:

```py
tshirts = [(color, size) for color in colors for size in sizes]
```

## <a name="gen">Generator</a>

```py
tshirts = (color for color in colors)

tuple(ord(symbol) for symbol in symbols)
```

## <a name="colas">Colas</a>

```py
from collections import deque

dq = deque(range(10), maxlen=10)  

dq.rotate(3)  
dq.rotate(-4)

dq.append(val)
dq.appendleft(val)  

dq.extend([val1, val2, val3])  
dq.extendleft([val1, val2, val3])  

dq.insert(pos, val)

dq.remove(val)

dq.pop()
dq.popleft()

dq.index(val)

dq.clear()

dq.copy()

dq.count()

dq.reverse()

dq.sort([key], [reverse])
```

Otros paquetes:
- queue
- multiprocessing
- asyncio

### queue

```py
from collections import queue
```

This provides the synchronized (i.e., thread-safe) classes SimpleQueue, Queue, LifoQueue, and PriorityQueue. These can be used for safe communication between threads. All except SimpleQueue can be bounded by providing a maxsize argument greater than 0 to the constructor. However, they don’t discard items to make room as deque does. Instead, when the queue is full the insertion of a new item blocks—i.e., it waits until some other thread makes room by taking an item from the queue, which is useful to throttle the number of live threads

### multiprocessing

```py
from collections import multiprocessing
```

Implements its own unbounded SimpleQueue and bounded Queue, very similar to those in the queue package, but designed for interprocess communication. A specialized multiprocessing.JoinableQueue is provided for task management

### asyncio

```py
from collections import asyncio
```

Provides Queue, LifoQueue, PriorityQueue, and JoinableQueue with APIs inspired by the classes in the queue and multiprocessing modules, but adapted for managing tasks in asynchronous programming

## <a name="patron">Pattern Matching</a>

```py
def get_creators(record: dict) -> list:
    match record:
        case {'type': 'book', 'api': 2, 'authors': [*names]}:  
            return names
        case {'type': 'book', 'api': 1, 'author': name}:  
            return [name]
        case {'type': 'book'}:  
            raise ValueError(f"Invalid 'book' record: {record!r}")
        case {'type': 'movie', 'director': name}:  
            return [name]
        case _:  
            raise ValueError(f'Invalid record: {record!r}')
```

## <a name="copia">Copy</a>

Cuando igualamos una variable a otra, lo que estamos haciendo es establecer creando una referencia a la misma posición de memoria.

```py
charles = {'name': 'Charles L. Dodgson', 'born': 1832}
lewis = charles  

lewis is charles
True

id(charles), id(lewis)  
(4300473992, 4300473992)
```

Si creamos otro diccionario con los mismos valores, la referencia es diferente:

```py
alex = {'name': 'Charles L. Dodgson', 'born': 1832, 'balance': 950}  

alex == charles  
True

alex is not charles  
True
```

`is` compara los hashes de las dos variables, y estos son diferentes. `==` compara los valores tal y como se hayan definido en \_\_eq\_\_. `a==b` es equivalente a `a.__eq__(b)`.

Habitualmente nos interesará usar `==`, aunque hay una referencia muy utilizada, `None` que usaremos con `is`.

Para copiar una lista la forma más sencilla es hacer `copia=list(original)`. La copia es por defecto _swallow_. Esto significa que `copia` y `original` seran dos referencias diferentes, pero los valores serán los mismos. Esto, es si alguno de los elementos de la lista es mutable, cambiandolo a tráves de `original` estaremos afectando a `copia`.

```py
l1 = [3, [55, 44], (7, 8, 9)]
l2 = list(l1)  

l2 == l1  
True

l2 is l1  
False
```

Haciendo `l2 = l1[:]` conseguimos el mismo efecto.

Si tenemos:

```py
l1 = [3, [66, 55, 44], (7, 8, 9)]
l2 = list(l1)      
```

No se vera en l2, porque hemos añadido un elemento más a la primera referencia:

```py
l1.append(100)     
```

El elemento `[1]` es mutable, así que si lo modificamos la referencia que tenemos en `l1[1]` no cambia, y esta es la misma referencia que tenemos en `l2[1]`. Estos cambios son visibles pués tanto desde `l1` como desde `l2`: 

```py
l1[1].remove(55)   
l2[1] += [33, 22]
```
El elemento `l2[2]` esta apuntando a una tupla, que es inmutable. Esto significa que al hacer esta operación se está creando una nueva referencia para la tupla, es decir que `l2[2]` y `l1[2]` ya no apuntan al mismo sitio:

```py
l2[2] += (10, 11)  
```

### Shallow and Deep Copy

Si hacemos:

```py
class Bus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)
```

tenemos una variable de instancia, `self.passengers` que es una lista. Si al constructor le alimentamos con una lista, se crea una copia de la misma, esto es, una shallow copy. 

```py
import copy
bus1 = Bus(['Alice', 'Bill', 'Claire', 'David'])
bus2 = copy.copy(bus1)
bus3 = copy.deepcopy(bus1)
```

`bus1`y `bus2` son `==` pero no tienen el mismo `id`. `self.passengers`, el contenido, tendran el mismo `id`:

```py
id(bus1), id(bus2), id(bus3)
(4301498296, 4301499416, 4301499752)
```

Si ahora hacemos:

```py
bus1.drop('Bill')
```

Se vera refleajado en `bus2` pero no en `bus3`. Podemos ver como efectivamente la propiedad `passengers` de `bus1` y `bus2` es la misma, pero no así en `bus3`: 

```py
id(bus1.passengers), id(bus2.passengers), id(bus3.passengers)
(4302658568, 4302658568, 4302657800)
```

### referencias

Los argumentos se pasan a las funciones siempre por referencia. Esto significa que cuando los argumentos se refieran a tipos mutables, una modificación del argumento será _visible_ fuera del método.

# <a name="esp">Special methods</a>

The `__builtins__.__dict__` stores all built-in types, objects, and functions.

## `__iadd__` y `__add__`

The special method that makes += work is `__iadd__` (for “in-place addition”). However, if. `__iadd__` is not implemented, Python falls back to calling `__add__`.

## Hasheable

An object is hashable if it has a hash code which never changes during its lifetime (it needs a `__hash__()` method), and can be compared to other objects (it needs an `__eq__()` method). Hashable objects which compare equal must have the same hash code

## Lista

```py
    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]
```

## `__call__`

Para crear un tipo como callable se implementa \_\_call\_\_:

```py
import random

class BingoCage:

    def __init__(self, items):
        self._items = list(items)  
        random.shuffle(self._items)  

    def pick(self):  
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')  

    def __call__(self):  
        return self.pick()

bingo = BingoCage(range(3))
bingo.pick()
```

Podemos hacer usar `bingo` como si se tratara de una función:

```py
bingo()
```

# <a name="dicc">Diccionario</a>

Métodos que hacen de un diccionario un diccionario:

```py
d.__contains__(k). Implementa `in`
d.__delitem__(k)
d.__getitem__(k). Implementa `[x]`
d.__iter__().
d.__len__()
d.__missing__(k). Este método es llamado cuando hacemos un `[x]` y el índice no existe
d.__reversed__()
d.__setitem__(k, v)
```

Ejemplo de creacion de un tipo de diccionario custom:

```py
class StrKeyDict0(dict):  
    def __missing__(self, key):
		if isinstance(key, str):  
            raise KeyError(key)
        return self[str(key)]  

    def get(self, key, default=None):
        try:
            return self[key]  
        except KeyError:
            return default  

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()
```

Lo mismo pero usando `UserDict`:

```py
import collections

class StrKeyDict(collections.UserDict):  

    def __missing__(self, key):  
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data  

    def __setitem__(self, key, item):
        self.data[str(key)] = item
```

## collections.Counter

```py
ct = collections.Counter('abracadabra')

ct
Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

ct.update('aaaaazzz')

ct
Counter({'a': 10, 'z': 3, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

ct.most_common(3)
[('a', 10), ('z', 3), ('b', 2)]
```

# <a name="set">Set y frozenset</a>

Podemos crear un set a partir de una lista:

```py
l = ['spam', 'spam', 'eggs', 'spam', 'bacon', 'eggs']

set(l)
{'eggs', 'spam', 'bacon'}
```

Podemos crear una lista a partir de un set:

```py
list(set(l))
['eggs', 'spam', 'bacon']
```

El set nos permite hacer operaciones de conjuntos. Por ejemplo, aquí hacemos la intersección de dos conjuntos:

```py
found = len(set(needles) & set(haystack))
```

Otras operaciones disponibles:

|operador|magic|descripcion|
|----|----|----|
|s ^ z|`s.__xor__(z)`|Symmetric difference (the complement of the intersection s & z)|
|s <= z|`s.__le__(z)`|s is a subset of the z set|
|s < z|`s.__lt__(z)`|s is a proper subset of the z set|
|s >= z|`s.__ge__(z)`|s is a superset of the z set|
|e in s|`s.__contains__(e)`|Element e is a member of s|
|s > z|`s.__gt__(z)`|s is a proper superset of the z set|
|s & z|`s.__and__(z)`|Intersection of s and z|
|z & s|`s.__rand__(z)`|Reversed & operator|
|s &= z|`s.__iand__(z)`|s updated with intersection of s and z|
|s | z|`s.__or__(z)`|Union of s and z|
|z | s|`s.__ror__(z)`|Reversed or|

Podemos ver las diferencias entre `sets` y `frozensets`:

|operacion|set|frozenset|descripcion|
|----|----|----|----|
|s.add(e)|x||Add element e to s|
|s.clear()|x|||Remove all elements of s|
|s.copy()|x|x|Shallow copy of s|
|s.discard(e)|x||Remove element e from s if it is present|
|`s.__iter__()`|x|x|Get iterator over s|
|`s.__len__()`|x|x|len(s)|
|s.pop()|x||Remove and return an element from s, raising KeyError if s is empty|
|s.remove(e)|x||Remove element e from s, raising KeyError if e not in s|

Las vista obtenida por lo métodos .keys() y .items() de un diccionario se parecen mucho a un `frozenset`. Especialmente podemos hacer uso de las operacione de intersección, unión, etc:

```py
d1 = dict(a=1, b=2, c=3, d=4)
d2 = dict(b=20, d=40, e=50)

d1.keys() & d2.keys()
{'b', 'd'}


s = {'a', 'e', 'i'}
d1.keys() & s
{'a'}

d1.keys() | s
{'a', 'c', 'b', 'd', 'i', 'e'}
```

# <a name="clases">Implementar Clases</a>

Tenemos dos técnicas con las que podemos crear clases que incorporen los _ingredientes típicos_ de un objeto, como `__repr__` y `__eq__`:

- namedtuple
- typed namedtuple. Similar al anterior, pero tipitficando los mienbros de la clase
- dataclass

## namedtuples

Incluye una implementación de `repr` y `eq`:

```py
from collections import namedtuple

Coordinate = namedtuple('Coordinate', 'lat lon')

issubclass(Coordinate, tuple)
True

moscow = Coordinate(55.756, 37.617)
moscow
Coordinate(lat=55.756, lon=37.617)  

moscow == Coordinate(lat=55.756, lon=37.617)  
True
```

Naturalmente tambien podemos crear una subclase de `namedtuple` y así incluir otros métodos custom.

## typed namedtuples

Similar al namedtuple pero tipitificamos los atributos:

```py
import typing

Coordinate = typing.NamedTuple('Coordinate', [('lat', float), ('lon', float)])

issubclass(Coordinate, tuple)
True

typing.get_type_hints(Coordinate)
{'lat': <class 'float'>, 'lon': <class 'float'>}
```

## dataclass

```py
@dataclass(*, init=True, repr=True, eq=True, order=False,unsafe_hash=False, frozen=False)
```

|parametro|significado|defecto|descripcion|
|----|----|----|----|
|init|generate `__init__`|True|Ignored if `__init__` is implemented by user.|
|repr|generate `__repr__`|True|Ignored if `__repr__` is implemented by user.|
|eq|generate `__eq__`|True|Ignored if `__eq__` is implemented by user.|
|order|generate `__lt__`, `__le__`, `__gt__`, `__ge__`|False|If True, raises exceptions if eq=False, or if any of the comparison methods that would be generated are defined or inherited.|
|unsafe_hash|generate __hash__|False|Complex semantics and several caveats—see: dataclass documentation.|
|frozen|make instances “immutable”|False|instances will be reasonably safe from accidental change, but not really immutable|

If the eq and frozen arguments are both True, @dataclass produces a suitable `__hash__` method, so the instances will be hashable. The generated `__hash__` will use data from all fields that are not individually excluded using a field option we’ll see in `Field options`. If frozen=False (the default), @dataclass will set `__hash__` to None, signalling that the instances are unhashable, therefore overriding `__hash__` from any superclass.


```py
from dataclasses import dataclass, field


@dataclass
class ClubMember:
    name: str
    guests: list = field(default_factory=list)
```

### field

A la hora de fijar valores por defecto, podemos usar `field` para controlar el comportamiento, no solo del valor por defecto, pero que queremos que se haga con el campo en cuestion, si se debe considerar a la hora de generar otros métodos "mágicos":

|parametro|significado|defecto|descripcion|
|----|----|----|----|
|default|default value for field||
|default_factory|0-parameter function used to produce a default||
|init|include field in parameters to `__init__`|True|
|repr|include field in `__repr__`|True|
|compare|use field in comparison methods `__eq__`, `__lt__` etc.|True|
|hash|include field in `__hash_` calculation|will be included only if compare is True|
|metadata|mapping with user-defined data; ignored by the @dataclass||

### `__post_init__`

The `__init__` method generated by @dataclass only takes the arguments passed and assigns them—or their default values, if missing—to the instance attributes that are instance fields. But you may need to do more than that to initialize the instance. If that’s the case, you can provide a `__post_init__` method. When that method exists, @dataclass will add code to the generated `__init__` to call `__post_init__` as the last step.

Common use cases for `__post_init__` are validation and computing field values based on other fields. We’ll study a simple example that uses `__post_init__` for both of these reasons.

```py
from dataclasses import dataclass
from club import ClubMember

@dataclass
class HackerClubMember(ClubMember):                         
    all_handles = set()                                     
    handle: str = ''                                        

    def __post_init__(self):
        cls = self.__class__
		if self.handle == '':                               
            self.handle = self.name.split()[0]
        if self.handle in cls.all_handles:                  
            msg = f'handle {self.handle!r} already exists.'
            raise ValueError(msg)
        cls.all_handles.add(self.handle)
```

### Typed class attributes

`ClassVar` nos permite usar la notación de `generics`, `[]`, para definir tipos. Por ejemplo, para indicar que una variable es un set de strings:

all_handles: ClassVar[set[str]] = set()

### InitVar

Cuando queremos usar una variable en el constructor pero que no queremos que se convierta en un campo de la instancia, podemos usr en el tipo InitVar. En este ejemplo, la variable `database` es de tipo `DatabaseType` y no será creada como un campo de la instancia. El valor que se pase a `__init__` será pasado a su vez a `__post_init__` - si existiera un `__post_init__`:

```py
@dataclass
class C:
    i: int
    j: int = None
    database: InitVar[DatabaseType] = None

    def __post_init__(self, database):
        if self.j is None and database is not None:
            self.j = database.lookup('j')

c = C(10, database=my_database)
```

Pero en `dataclasses.fields` no se incluirá esta variable.

## Resumen

|namedtuple|type namedtuple|dataclass|descripcion|
|------|------|------|------|
|x._fields|x._fields|[f.name for f in dataclasses.fields(x)]|Nombre de los campos de una clase. Es una tupla que obtenemos a partir de un tipo|
|x._field_defaults|x._field_defaults|[f.default for f in dataclasses.fields(x)]|Diccionario con todos los valores por defecto de una clase. Es un diccionario que obtenemos a partir de un tipo|
|`x.__annotations__`|`x.__annotations__`|new instance with changes|Tipos definidos en la clase|
|x._asdict()|x._asdict()|dataclasses.asdict(x)|Diccionario con todos los campos y valores de una instancia. es un diccionario|
|x._replace(…)|x._replace(…)|dataclasses.replace(x, …)|Reemplaza el contenido de una instancia|
|_make(iterable)|_make(iterable)|_make(iterable)|Crea una instancia con el diccionario|

Creamos una clase:

```py
from collections import namedtuple

City = namedtuple('City', 'name country population coordinates')  
```

Creamos una instancia:

```py
tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))  

tokyo
City(name='Tokyo', country='JP', population=36.933, coordinates=(35.689722,139.691667))

tokyo.population  
36.933

tokyo.coordinates
(35.689722, 139.691667)

tokyo[1]
'JP'
```

Los campos de la clase:

```py
City._fields  
('name', 'country', 'population', 'location')
```

Vamos a crear una instancia con un diccionario:

```py
Coordinate = namedtuple('Coordinate', 'lat lon')
delhi_data = ('Delhi NCR', 'IN', 21.935, Coordinate(28.613889, 77.208889))
delhi = City._make(delhi_data)  
```

Podemos ver los campos de la instancia:

```py
delhi._asdict()  
{'name': 'Delhi NCR', 'country': 'IN', 'population': 21.935, 'location': Coordinate(lat=28.613889, lon=77.208889)}
```

podemos usarlos para crear un json:

```py
import json
json.dumps(delhi._asdict())  
'{"name": "Delhi NCR", "country": "IN", "population": 21.935, "location": [28.613889, 77.208889]}'
```

Podemos ver los valores por defecto:

```py
Coordinate = namedtuple('Coordinate', 'lat lon reference', defaults=['WGS84'])
Coordinate(0, 0)
Coordinate(lat=0, lon=0, reference='WGS84')

Coordinate._field_defaults
{'reference': 'WGS84'}
```
 
# <a name="func">Functional programming</a>

Una función que acepta como argumento una función y/o devuelve una función. _Reduce_ toma una función y retorna un valor:

```py
from functools import reduce

def factorial(n):
    return reduce(lambda a, b: a*b, range(1, n+1))
```

Podemos usar también `map` y `filter`:

```py
list(map(factorial, range(11)))
[1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]

list(map(factorial, filter(lambda n: n % 2, range(6))))  
[1, 6, 120]
```

Son equivalentes a:

```py
[factorial(n) for n in range(6)]  
[1, 1, 2, 6, 24, 120]

[factorial(n) for n in range(6) if n % 2]  
[1, 6, 120]
```

Otras funciones que se usan con frecuencia son `any` y `all`.

## Operadores

Podemos evitar tener que usar lambdas empleando alguno de los operadores definidos en el paquete _operator_: 

```py
from functools import reduce
from operator import mul

def factorial(n):
    return reduce(mul, range(1, n+1))
```

### itemgetter

_itemgetter_ nos permite acceder al operador `[]` en aquellos tipos que definen \_\_getitem\_\_. En este ejemplo ordenamos los datos por el elemento `[1]`:

```py
metro_data = [
     ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
     ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
     ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
     ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
     ('São Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
 ]

from operator import itemgetter

for city in sorted(metro_data, key=itemgetter(1)):
    print(city)	
```

### attrgetter

De forma similar podemos usar _attrgetter_. Por ejemplo, definimos un tipo llamado `LatLon`:

```py
from collections import namedtuple

LatLon = namedtuple('LatLon', 'lat lon')  
Metropolis = namedtuple('Metropolis', 'name cc pop coord')  

metro_areas = [Metropolis(name, cc, pop, LatLon(lat, lon)) for name, cc, pop, (lat, lon) in metro_data]
```

```py
metro_areas[0]
Metropolis(name='Tokyo', cc='JP', pop=36.933, coord=LatLon(lat=35.689722, lon=139.691667))

metro_areas[0].coord.lat  
35.689722
```

Veamos como podemos usar _attrgetter_:

```py
from operator import attrgetter

name_lat = attrgetter('name', 'coord.lat')  
```

Hemos definido a la función - operador - _name\_lat_ como los campos _name_ y _coord.lat_. Esto devolvera una dupla con estos dos valores. Aqí lo usamos para ordenar, y para recuperar el valor:

```py
for city in sorted(metro_areas, key=attrgetter('coord.lat')):
    print(name_lat(city))  
('São Paulo', -23.547778)
('Mexico City', 19.433333)
('Delhi NCR', 28.613889)
('Tokyo', 35.689722)
('New York-Newark', 40.808611)
```

### methodcaller

Otro operador _curioso_ es `methodcaller`. Nos permite invocar métodos, con y sin argumentos:

```py
from operator import methodcaller

s = 'The time has come'
upcase = methodcaller('upper')

upcase(s)
'THE TIME HAS COME'

hyphenate = methodcaller('replace', ' ', '-')
hyphenate(s)
'The-time-has-come'
```

### partial

Podemos definir con partial una implementación parcial de un operador. Por ejemplo, podemos definir una variante del operador `mul` que se utilice para triplicar el valor:

```py
from operator import mul
from functools import partial

triple = partial(mul, 3)  
```

Podemos usar el operador:

```py
triple(7)  
21

list(map(triple, range(1, 10)))  
[3, 6, 9, 12, 15, 18, 21, 24, 27]
```

# <a name="hint">Hints</a>

## mypy

```ps
pip install mypy

mypy messages.py
```

Podemos exigir que no haya variables sin tipar:

```ps
mypy --disallow-untyped-defs messages_test.py
```

Podemos ser menos extrictos, y simplemente pedir que una vez en una función se tipifique algún argumento, se tipifiquen todos. Esto nos permite ser más graduales a la hora de tipificar cosas:

```ps
mypy --disallow-incomplete-defs messages_test.py
```

Podemos definir los tipos con el operador `:`:

```py
def show_count(count: int, singular: str, plural: Optional[str] = None) -> str:
```

```py
def double(x):
    return x * 2
```

The x parameter type may be numeric (int, complex, Fraction, numpy.uint32 etc.) but it may also be a sequence (str, tuple, list, array), an N-dimensional numpy.array or any other type that implements or inherits a `__mul__` method that accepts an int argument.

Esto por ejemplo fallará porque _abc.Sequence_ no incluye `__mul__`:

```py
from collections import abc

def double(x: abc.Sequence):
    return x * 2
```

A la hora de tipar podemos usar:

- typing.Any;
- Simple types and classes;
- typing.Optional and typing.Union;
- Generic collections, including tuples and mappings;
- Abstract Base Classes;
- Generic iterables;
- Parameterized generics and TypeVar;
- typing.Protocols — the key to static duck typing;
- typing.Callable;
- typing.NoReturn

## Any

Es el comodin, dara por buena cualquier cosa que hagamos. Por ejemplo, esta definición sera considerada válida:

```py
def double(x: Any) -> Any:
    return x * 2
```

Si hubieramos hecho:

```py
def double(x: object) -> object:
    return x * 2
```

Se habría marcado un error porque _object_ no implementa `__mul__`.

## Simple types and classes

```py
class T1:
    ...

class T2(T1):
    ...
```

Esto sería correcto:

```py
def f1(p: T1) -> None:
    ...

o2 = T2()

f1(o2)
```

Esto __no sería__ correcto:

```py
def f2(p: T2) -> None:
    ...

o1 = T1()

f2(o1)
```

## typing.Optional and typing.Union

Optional:  
```py
from typing import Optional

def show_count(count: int, singular: str, plural: Optional[str] = None) -> str:
```

`Optional[str]` equivale a `Union[str, None]`:

```py
from typing import Union

def parse_token(token: str) -> Union[str, float]:
    try:
        return float(token)
    except ValueError:
        return token
```

## Generic collections

```py
def tokenize(text: str) -> list[str]:
    return text.upper().split()
```

Las colecciones que pueden anotarse de esta forma son:

- list
- collections.deque
- set
- frozenset
- Iterator[str]
- abc.Sequence
- abc.MutableSequence 
- abc.Container
- abc.Set
- abc.MutableSet
- abc.Collection

## tuplas

Las tuplas se anotan como sigue:

```py
def geohash(lat_lon: tuple[float, float]) -> str:  
    return gh.encode(*lat_lon, PRECISION)
```

Otro ejemplo:

```py
from collections.abc import Sequence

def columnize(sequence: Sequence[str], num_columns: int = 0) -> list[tuple[str, ...]]:
    if num_columns == 0:
        num_columns = round(len(sequence) ** .5)
        num_rows, reminder = divmod(len(sequence), num_columns)
    num_rows += bool(reminder)
    return [tuple(sequence[i::num_rows]) for i in range(num_rows)]
```

## Generic mappings

Podemos anotar un diccionario como `MappingType[KeyType, ValueType]` o como `dict[str, set[str]]`.

## Abstract Base Classes (abc)

Si declaramos lo siguiente:

```py
from collections.abc import Mapping

def name2hex(name: str, color_map: Mapping[str, int]) -> str:
```

Al usar `abc.Mapping` podemos pasar una instancia de `dict`, `defaultdict`, `ChainMap`, una hija de `UserDict`. Si usaramos:

```py
def name2hex(name: str, color_map: dict[str, int]) -> str:
```

La definición es mucho más restrictiva, el argumento tiene que ser si o si un `dict`.

## Generics

Podemos definir un genéric usando `TypeVar`:
```py
from collections.abc import Sequence
from random import shuffle
from typing import TypeVar

T = TypeVar('T')

def sample(population: Sequence[T], size: int) -> list[T]:
    if size < 1:
        raise ValueError('size must be >= 1')
    result = list(population)
    shuffle(result)
    return result[:size]
```

Podemos ser más especificos al definir el genérico:

```py
from collections.abc import Iterable
from decimal import Decimal
from fractions import Fraction
from typing import TypeVar

NumberT = TypeVar('NumberT', float, Decimal, Fraction)

def mode(data: Iterable[NumberT]) -> NumberT:
```

aquí hemos dicho que el genérico tiene que ser un `float`, `Decimal` o `Fraction`. Podemos tambien hacer que el generic sea una subclase:

```py
from collections import Counter
from collections.abc import Iterable, Hashable
from typing import TypeVar

HashableT = TypeVar('HashableT', bound=Hashable)

def mode(data: Iterable[HashableT]) -> HashableT:
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError('no mode for empty data')
    return pairs[0][0]
```

estamos diciendo que el genérico tiene que ser una subclase de `Hashable`.

## Callable

Indicamos la lista de argumentos y el tipo que devuelbe la función:

```py
def repl(input_fn: Callable[[Any], str] = input) -> None:
```

# <a name="dec">Decorators</a>

Los decorators se cargan al importar el modulo en el que estan definidos:

```py
registry = []  

def register(func):  
    print(f'running register({func})')  
    registry.append(func)  
    return func  

a=0

@register
def f1(v1):
    global a
    a=v1
    print('running f1()')

@register
def f2():
    global a
    a+=1
    print('running f2()')

def f3(a):  
    global a
    print(a)
    print('running f3()')

def main():  
    print('running main()')
    print('registry ->', registry)
    f1()
    f2()
    f3()

if __name__ == '__main__':
    main()  
```

Podemos usar dos keywords para especificar el scope:
- global. Indicamos que la variable que usaremos tiene scope global
- nolocal. Indicamos que la variable que usaremos no esta definida de forma local. Será una variable definida en la closure

## functools.wraps

Con `functools.wraps` hacemos que nuestro wrapper _"respete"_ el `__doc__` y `__name__` de la función original:

```py
import time
import functools


def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_lst = [repr(arg) for arg in args]
        arg_lst.extend(f'{k}={v!r}' for k, v in kwargs.items())
        arg_str = ', '.join(arg_lst)
        print(f'[{elapsed:0.8f}s] {name}({arg_str}) -> {result!r}')
        return result
    return clocked
```

## Cache

```py
import functools

from clockdeco import clock


@functools.cache  
@clock  
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)

@lru_cache(maxsize=2**20, typed=True)
def fibonacci2(n):
    if n < 2:
        return n
    return fibonacci2(n - 2) + fibonacci2(n - 1)

if __name__ == '__main__':
    print(fibonacci(6))
```

## Parametrized Decorator

Podemos definir parametros en el decorador:

```py
import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

def clock(fmt=DEFAULT_FMT):  
    def decorate(func):      
        def clocked(*_args): 
            t0 = time.perf_counter()
            _result = func(*_args)  
            elapsed = time.perf_counter() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)  
            result = repr(_result)  
            print(fmt.format(**locals()))  
            return _result  
        return clocked  
    return decorate  

if __name__ == '__main__':
    @clock('{name}: {elapsed}s') 
    def snooze(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze(.123)
```

Una forma más elegante de conseguir este mismo efecto es a través de una clase que recoja en su constructos los parámetros:

```py
import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

class clock:  

    def __init__(self, fmt=DEFAULT_FMT):  
        self.fmt = fmt
    
    def __call__(self, func):  
        def clocked(*_args):
            t0 = time.perf_counter()
            _result = func(*_args)  
            elapsed = time.perf_counter() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result)
            print(self.fmt.format(**locals()))
            return _result
        return clocked
```

# <a name="modelado">Modelado de Objetos</a>

## Implementation of the Order class with pluggable discount strategies

Declaramos las clases base como subclases de `NamedTuple`. Esto nos permite definir algún método dentro de la clase:

```py
from abc import ABC, abstractmethod
from collections.abc import Sequence
from decimal import Decimal
from typing import NamedTuple, Optional


class Customer(NamedTuple):
    name: str
    fidelity: int

class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal
    
    def total(self) -> Decimal:
        return self.price * self.quantity
```

El pedido esta formado por una lista de `LineItem`. Lo tipificamos como __`Sequence`__ para poder definir cart como __strings, lists, tuples, byte sequences, byte arrays, o range objects__. También fijemonos en `__repr__`, como retornamos una _f-string_:

```py
class Order(NamedTuple):  # the Context
    customer: Customer
    cart: Sequence[LineItem]
    promotion: Optional['Promotion'] = None

    def total(self) -> Decimal:
        totals = (item.total() for item in self.cart)
        return sum(totals, start=Decimal(0))

    def due(self) -> Decimal:
        if self.promotion is None:
            discount = Decimal(0)
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        return f'<Order total: {self.total():.2f} due: {self.due():.2f}>'
```

en este patrón de diseño damos pie a que se usen diferentes tipos de promociones definiendo un tipo abstracto, `Promotion`. Este tipo abstracto tiene un método llamado `discount` que toma por argumento una `Order` - `self.promotion.discount(self)`. Podemos verlo también en la definición:

```py
class Promotion(ABC):  # the Strategy: an abstract base class
    @abstractmethod
    def discount(self, order: Order) -> Decimal:
        """Return discount as a positive dollar amount"""
```

podemos definir diferentes tipos de promociones como subclases de `Promotion`:

```py
class FidelityPromo(Promotion):  # first Concrete Strategy
    """5% discount for customers with 1000 or more fidelity points"""

    def discount(self, order: Order) -> Decimal:
        rate = Decimal('0.05')
        if order.customer.fidelity >= 1000:
            return order.total() * rate
        return Decimal(0)
```

otra más:

```py
class BulkItemPromo(Promotion):  # second Concrete Strategy
    """10% discount for each LineItem with 20 or more units"""

    def discount(self, order: Order) -> Decimal:
        discount = Decimal(0)
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * Decimal('0.1')
        return discount
```

y otra:

```py
class LargeOrderPromo(Promotion):  # third Concrete Strategy
    """7% discount for orders with 10 or more distinct items"""

    def discount(self, order: Order) -> Decimal:
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * Decimal('0.07')
        return Decimal(0)
```

Por ejemplo, si tenemos estos clientes y este carrito:

```ps
joe = Customer('John Doe', 0)  
ann = Customer('Ann Smith', 1100)
cart = (LineItem('banana', 4, Decimal('.5')),  
    LineItem('apple', 10, Decimal('1.5')),
    LineItem('watermelon', 5, Decimal(5)))
```

Podemos ahora crear diferentes pedidos:

```ps
Order(joe, cart, FidelityPromo())  
<Order total: 42.00 due: 42.00>

Order(ann, cart, FidelityPromo())  
<Order total: 42.00 due: 39.90>

banana_cart = (LineItem('banana', 30, Decimal('.5')),  
                LineItem('apple', 10, Decimal('1.5')))

Order(joe, banana_cart, BulkItemPromo())  
<Order total: 30.00 due: 28.50>

long_cart = tuple(LineItem(str(sku), 1, Decimal(1)) 
                  for sku in range(10))

Order(joe, long_cart, LargeOrderPromo())  
<Order total: 10.00 due: 9.30>

Order(joe, cart, LargeOrderPromo())
<Order total: 42.00 due: 42.00>
```

## Function-Oriented Strategy

```py
@dataclass(frozen=True)
class Order:  # the Context
    customer: Customer
    cart: Sequence[LineItem]
    promotion: Optional[Callable[['Order'], Decimal]] = None  

    def total(self) -> Decimal:
        totals = (item.total() for item in self.cart)
        return sum(totals, start=Decimal(0))

    def due(self) -> Decimal:
        if self.promotion is None:
            discount = Decimal(0)
        else:
            discount = self.promotion(self)  
        return self.total() - discount

    def __repr__(self):
        return f'<Order total: {self.total():.2f} due: {self.due():.2f}>'
```

y definimos ahora las funciones:

```py
def fidelity_promo(order: Order) -> Decimal:  
    """5% discount for customers with 1000 or more fidelity points"""
    if order.customer.fidelity >= 1000:
        return order.total() * Decimal('0.05')
    return Decimal(0)


def bulk_item_promo(order: Order) -> Decimal:
    """10% discount for each LineItem with 20 or more units"""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal('0.1')
    return discount


def large_order_promo(order: Order) -> Decimal:
    """7% discount for orders with 10 or more distinct items"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal('0.07')
    return Decimal(0)
```

para usarla:

```ps
Order(joe, cart, fidelity_promo)  
<Order total: 42.00 due: 42.00>
```

## Globals

Vamos a añadir una capacidad a la clase, la de aplicar la promoción más beneficiosa entre todas las disponibles.

Usamos `globals` para recuperar todos los items del modulo. Necesitamos aplicar un criterio de nomenclatura, que las funciones tengan comio sufijo `_promo`:

```py
from decimal import Decimal
from strategy import Order
from strategy import (
    fidelity_promo, bulk_item_promo, large_order_promo  
)

promos = [promo for name, promo in globals().items()  
                if name.endswith('_promo') and        
                   name != 'best_promo'               
]


def best_promo(order: Order) -> Decimal:              
    """Compute the best discount available"""
    return max(promo(order) for promo in promos)
```


## Introspection

Una alternativa a usar globals sería emplear introspection:

```py
from decimal import Decimal
import inspect
```

Recuperamos todos los items que sean funciones del módulo llamado `promotions`. Aquí el criterio es el de registrar todas las promociones en el módulo `promotions`.

```py
from strategy import Order
import promotions

promos = [func for _, func in inspect.getmembers(promotions, inspect.isfunction)]

def best_promo(order: Order) -> Decimal:
    """Compute the best discount available"""
    return max(promo(order) for promo in promos)
```

## Decorador

Podemos identificar las promociones usando un decorador. Definimos una lista que contendrá todas las Promociones, definidas estas como funciones que toman una _Order_ como argumento y retornan un _Decimal_:

```py
Promotion = Callable[[Order], Decimal]

promos: list[Promotion] = []  
```

Definimos la anotación:

```py
def promotion(promo: Promotion) -> Promotion:  
    promos.append(promo)
    return promo
```

ahora ya solo queda anotar las promociones:

```py
def best_promo(order: Order) -> Decimal:
    """Compute the best discount available"""
    return max(promo(order) for promo in promos)  

@promotion  
def fidelity(order: Order) -> Decimal:
    """5% discount for customers with 1000 or more fidelity points"""
    if order.customer.fidelity >= 1000:
        return order.total() * Decimal('0.05')
    return Decimal(0)

@promotion
def bulk_item(order: Order) -> Decimal:
    """10% discount for each LineItem with 20 or more units"""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
                     discount += item.total() * Decimal('0.1')
    return discount

@promotion
def large_order(order: Order) -> Decimal:
    """7% discount for orders with 10 or more distinct items"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal('0.07')
    return Decimal(0)
```

# <a name="ABC">Clases Abstractas</a>

![ABCs](./imagenes/ABCs.png)

- __Iterable, Container, Sized__

__Every collection should either inherit from these ABCs or implement compatible protocols__. __Iterable__ supports iteration with `__iter__`, __Container__ supports the in operator with `__contains__`, and __Sized__ supports len() with `__len__`.

- __Collection__

This ABC __has no methods of its own__, but was added in Python 3.6 __to make it easier to subclass from Iterable, Container, and Sized__.

- __Sequence, Mapping, Set__

These are the __main immutable collection types__, and each has a mutable subclass.

![Secuencias](./imagenes/Secuencias.png)

- __MappingView__

In Python 3, the __objects returned from the mapping methods .items(), .keys(), and .values() implement the interfaces defined in ItemsView, KeysView, and ValuesView__, respectively. The first two also implement the rich interface of Set, with all the operators we saw in “Set Operations”.

- __Iterator__

Note that iterator subclasses Iterable.

- __Callable, Hashable__

These are not collections, but collections.abc was the first package to define ABCs in the standard library, and these two were deemed important enough to be included. They support type checking objects that must be callable or hashable.

## Implementation tips

- An abstract method can actually have an implementation. Even if it does, subclasses will still be forced to override it, but they will be able to invoke the abstract method with super(), adding functionality to it instead of implementing from scratch. 
- The best way to declare an ABC is to subclass abc.ABC or any other ABC
- A __virtual subclass of an ABC__. This is done by calling a register class method on the ABC. The registered class then becomes a virtual subclass of the ABC, and will be recognized as such by issubclass, but it does not inherit any methods or attributes from the ABC.

```py
from random import randrange

from tombola import Tombola

@Tombola.register  
class TomboList(list):  

    def pick(self):
        if self:  
            position = randrange(len(self))
            return self.pop(position)  
        else:
            raise LookupError('pop from empty TomboList')

    load = list.extend

    def loaded(self):
        return bool(self)  

    def inspect(self):
        return tuple(self)
```

__Tombolist is registered as a virtual subclass of Tombola__. Tombolist __extends list__. Tombolist inherits its boolean behavior from list, and that returns True if the list is not empty. __Tombolist.load is the same as list.extend__. We could also have registered the virtual class as follows:

```py
Tombola.register(TomboList)
```

# <a name="protocolo">Protocolos</a>

Para implementar un protocolo la clase tiene que heredar de `typing.Protocol`. En este ejemplo `Repeatable` es cualquier cosa que incluya un método `__mul__` que permita multiplicar un tipo `T` por un entero y retornar `T`:

```py
from typing import TypeVar, Protocol

T = TypeVar('T')  

class Repeatable(Protocol):
    def __mul__(self: T, repeat_count: int) -> T: ...  
```

Podemos usar el tipo en cualquier definición, por ejemplo, para definir una función:

```py
RT = TypeVar('RT', bound=Repeatable)  

def double(x: RT) -> RT:  
    return x * 2
```

When defining a typing.Protocol subclass, you can use the @runtime_checkable decorator to make that protocol support isinstance/issubclass checks at runtime

```py
@runtime_checkable
class SupportsComplex(Protocol):
    """An ABC with one abstract method __complex__."""
    __slots__ = ()

    @abstractmethod
    def __complex__(self) -> complex:
        pass
```

Si necesitamos un Protocolo que herede de otro protocolo, tenemos que incluir como base la clase de la que queremos heredar __y el propio Protocolo__:

```py
from typing import Protocol, runtime_checkable
from randompick import RandomPicker

@runtime_checkable  
class LoadableRandomPicker(RandomPicker, Protocol):  
    def load(self, Iterable) -> None: ...  
```
