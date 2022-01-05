class Coordenada_basic:
    lat: float
    lon: float=12.1
    otro='hola'

    #Tenemos que definir explicitamente el constructor
    def __init__(self,lat:float,lon:float,otro:str):
        self.lat=lat
        self.lon=lon
        self.otro=otro

from typing import NamedTuple

class Coordenada_typed_namedtuple(NamedTuple):
    lat: float
    lon: float=12.1
    otro='hola'

    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        we = 'E' if self.lon >= 0 else 'W'
        return f'{abs(self.lat):.1f}°{ns}, {abs(self.lon):.1f}°{we}'

from dataclasses import InitVar, dataclass, field
from typing import ClassVar
from collections import Set

#Atributos que se pueden especificar al anotar dataclass
#init.
@dataclass(frozen=False,init=True,eq=True,order=True,repr=True, unsafe_hash=True)
class Coordenada_dataclass:
    lat: float
    lon: float=12.1
    otro='hola'

    #Hacemos que se instancia este atributo con una lista, que será nueva en cada instancia
    lista:list=field(default_factory=list)

    #Especificamos un valor por defecto, además indicamos que queremos que la variable se use en init, repr, hash y en compare
    cadena:str=field(default="eugenio",init=True,repr=True,hash=True,compare=True)

    #Indicamos que el tipo de este argumento es un set de strings
    #miset: ClassVar[set[str]] = set()

    #Indicamos que esta variable no tiene que tratarse como cualquier otra variable,
    # no se inicializara como un miembro de la clase - self.no_en_init. Se pasara como argumento a Init
    # , y de Init se pasara a __post_init__
    no_en_init: InitVar[str]=field(default="pupa")

    def __post_init__(self, no_en_init:str):
        self.en_init=no_en_init


    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        we = 'E' if self.lon >= 0 else 'W'
        return f'{abs(self.lat):.1f}°{ns}, {abs(self.lon):.1f}°{we}'
