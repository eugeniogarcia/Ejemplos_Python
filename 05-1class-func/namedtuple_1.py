"""
# Demo named tuple

>>> from coordinates_3 import Coordinate
>>> moscow = Coordinate(55.76, 37.62)
>>> moscow # doctest:+ELLIPSIS
<coordinates.Coordinate object at ...
>>> location = Coordinate(55.76, 37.62)
>>> location == moscow
False

#Ahora con namedtuple. Implementa el __repr__ y el __eq__

>>> from collections import namedtuple                    
>>> Coordinate = namedtuple('Coordinate', ['lat', 'lon'])
>>> issubclass(Coordinate, tuple)
True
>>> moscow = Coordinate(55.756, 37.617)
>>> moscow                                                
Coordinate(lat=55.756, lon=37.617)
>>> moscow == Coordinate(lat=55.756, lon=37.617)
True

# Usando typed namedtuple

>>> import typing
>>> Coordinate = typing.NamedTuple('Coordinate', [('lat', float), ('lon', float)])
>>> issubclass(Coordinate, tuple)
True
>>> typing.get_type_hints(Coordinate)
{'lat': <class 'float'>, 'lon': <class 'float'>}
>>> moscow == Coordinate(lat=55.756, lon=37.617)
True
>>> moscow
Coordinate(lat=55.756, lon=37.617)

# Creamos una clase implementando __str__
>>> from coordinates_3 import Coordenadas   
>>> madrid=Coordenadas(12,14)
>>> madrid
Coordenadas(lat=12, lon=14)
>>> print(madrid)
12.0°N, 14.0°E

#usando dataclass

>>> from coordinates_3 import Coord
>>> Leon=Coord(12,14,"nico")
>>> Leon
Coord(lat=12, lon=14, en_init='pupa', lista=[], cadena='eugenio')
>>> print(Leon)
12.0°N, 14.0°E
>>> Leon==Coord(12,14,"nico")
True
>>> Leon.__annotations__
{'lat': <class 'float'>, 'lon': <class 'float'>, 'en_init': <class 'str'>, 'lista': <class 'list'>, 'cadena': <class 'str'>, 'all_handles': typing.ClassVar[set[str]], 'no_en_init': dataclasses.InitVar[str]}
>>> from coordinates_3 import Coordenadas
>>> pucela = Coordenadas(55.76, 37.62)
>>> dir(pucela)
['__add__', '__annotations__', '__class__', '__class_getitem__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__match_args__', '__module__', '__mul__', '__ne__', '__new__', '__orig_bases__', '__reduce__', '__reduce_ex__', '__repr__', '__rmul__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '_asdict', '_field_defaults', '_fields', '_make', '_replace', 'count', 'index', 'lat', 'lon']
>>> pucela._asdict()
{'lat': 55.76, 'lon': 37.62}
>>> pucela._field_defaults
{'lon': 12.1}
>>> pucela._fields
('lat', 'lon')
>>> pucela.__annotations__
{'lat': <class 'float'>, 'lon': <class 'float'>}
"""
