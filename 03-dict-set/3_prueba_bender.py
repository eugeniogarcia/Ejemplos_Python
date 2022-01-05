import json
from typing import Optional
from jsonbender import bend, K, S, OptionalS, F, Reduce, Filter, Forall, Context
from jsonbender.control_flow import If, Switch, Alternation
import math

# Básico
MAPPING = {
    'fullName':
    (S('customer', 'first_name') + K(' ') + S('customer', 'last_name')),
    'city': S('address', 'city'),
}

source = {
    'customer': {
        'first_name': 'Inigo',
        'last_name': 'Montoya',
        'Age': 24,
    },
    'address': {
        'city': 'Sicily',
        'country': 'Florin',
    },
}

result = bend(MAPPING, source)
print(f"Básico: {json.dumps(result)}\n")

#Mezcla indices y keys para llegar al valor referenciado en el  diccionario
MAPPING = {'val': S('a', 'deeply', 'nested', 0, 'value')}
ret = bend(MAPPING, {'a': {'deeply': {'nested': [{'value': 42}]}}})
print(f"Mezcla indices y claves: {json.dumps(ret)}\n")

#La referencia no existe en el diccionario
source = {'does': {'exist': 23}}
MAPPING_1 = {'val': OptionalS('does', 'not', 'exist')}
ret = bend(MAPPING_1, source)
print(f"Referencia no existe: {json.dumps(ret)}\n")

#La referencia no existe en el diccionario, pero aplica un valor por defecto
MAPPING_2 = {'val': OptionalS('does', 'not', 'exist', default=27)}
ret = bend(MAPPING_2, source)
print(f"Referencia no existe, pero usa un default: {json.dumps(ret)}\n")

#Usa funciones, F
MAPPING = {
    'total_number_of_keys':
    F(len),  #Aplica la funcion len sobre el diccionario
    'number_of_str_keys':
    F(lambda source: len([k for k in source.keys() if isinstance(k, str)])
      ),  #Aplica una lambda sobre el diccionario
    'price_truncated':
    S('price_as_str') >> F(float) >> F(
        int
    ),  #Aplica una funcion sobre un lookup del diccionario, y el resultado se lo pasa a otra funcion
}
ret = bend(MAPPING, {'price_as_str': '42.2', 'k1': 'v', 1: 'a'})
print(f"Usa Funciones: {json.dumps(ret)}\n")

#Asegura que cuando se capture un error (protect) cuando hay un error en la funcion
MAPPING_1 = {'sqrt': S('val') >> F(math.sqrt).protect()}
ret = bend(MAPPING_1, {'val': 4})
print(f"Aplica una función: {json.dumps(ret)}\n")

ret = bend(MAPPING_1, {'val': None})
print(f"Captura el error al aplicar la función: {json.dumps(ret)}\n")

MAPPING_2 = {'sqrt': S('val') >> F(math.sqrt).protect(-1)}
ret = bend(MAPPING_2, {'val': -1})
print(
    f"Captura el error al aplicar la función y devuelve un valor por defecto:{json.dumps(ret)}\n"
)

#Usa operandos
a = S('a')
b = S('b')
MAPPING = {'add': a + b, 'sub': a - b, 'mul': a * b, 'div': a / b}
ret = bend(MAPPING, {'a': 10, 'b': 5})
print(f"Usa operandos: {json.dumps(ret)}\n")

#Reduce
MAPPING = {'suma de valores': S('ints') >> Reduce(lambda acc, i: acc + i)}
ret = bend(MAPPING, {'ints': [1, 4, 7, 9]})
print(f"Reduce: {json.dumps(ret)}\n")

#Filtro
MAPPING = {'valores pares': S('ints') >> Filter(lambda i: i % 2 == 0)}
ret = bend(MAPPING, {'ints': range(5)})
print(f"Filtro: {json.dumps(ret)}\n")

#Forall
MAPPING = {'valores dobles': S('ints') >> Forall(lambda i: i * 2)}
ret = bend(MAPPING, {'ints': range(5)})
print(f"Forall: {json.dumps(ret)}\n")

#Lookups alternativos. Intenta varios lookups, y usa el primero que devuelva datos
b = Alternation(S(1), S(0), S('key1'))

print(f"Usa un Alternate a pelo:{b(['a', 'b'])}\n")  #  -> 'b'
print(f"Usa un Alternate a pelo:{b(['a'])}\n")  #  -> 'a'
try:
    b([])  #  -> TypeError
except TypeError:
    pass

try:
    b({})  #  -> KeyError
except KeyError:
    pass

print(f"Usa un Alternate a pelo:{b({'key1': 23})}\n")  # -> 23

#Usa lookup a pelo
c = S('key1')
print(f"Usa un lookup a pelo: {c({'key1': 23})}")

#Usa un if
if_ = If(S('country') == K('China'), S('first_name'), S('last_name'))
print(
    f"Usa un IF:{if_({'country': 'China', 'first_name': 'Li', 'last_name': 'Na'})}"
)
print(
    f"Usa un IF:{if_({'country': 'Brazil','first_name': 'Gustavo','last_name': 'Kuerten'})}"
)

#Usa un switch
b = Switch(S('service'), {
    'twitter': S('handle'),
    'mastodon': S('handle') + K('@') + S('server')
},
           default=S('email'))

print(
    f"Usa un Switch (twitter):{b({'service': 'twitter', 'handle': 'etandel'})}"
)
print(
    f"Usa un Switch (mastodon):{b({'service': 'mastodon','handle': 'etandel','server': 'mastodon.social'})}"
)

print(
    f"Usa un Switch (facebook):{b({'service': 'facebook','email': 'email@whatever.com'})}"
)

#Contexto
MAPPING = {
    'name': S('name'),
    'age': (Context() >> S('year')) - S('birthyear'),
}
source = {'name': 'Mary', 'birthyear': 1990}
ret = bend(MAPPING, source, context={'year': 2016})
print(f"Uso de contexto: {json.dumps(ret)}\n")

from pydantic import BaseModel


class Cliente(BaseModel):
    name: str
    vorname: str
    alte: Optional[int]


class Contrato(BaseModel):
    nummer: int
    kunde: Cliente


valor1 = {
    "nummer": 1234,
    "kunde": {
        "name": "Eugenio",
        "vorname": "Garcia San Martin"
    }
}
cont1 = Contrato(**valor1)

valor2 = {
    "nummer": 12345,
    "kunde": {
        "name": "Nicolas",
        "vorname": "Garcia",
        "alte": 30
    }
}
cont2 = Contrato(**valor2)

alte_ = If(S('kunde', 'alte') == K(None), K('n/a'), S('kunde', 'alte'))
mapa = {
    "nombre": S('kunde', 'name'),
    "apellido": S('kunde', 'vorname'),
    "contrato": S('nummer'),
    "edad": alte_,
    "edad bis": OptionalS('kunde', 'alte', default='n/a')
}
print(f"Valor transformado:{bend(mapa,cont1.dict())}")
print(f"Valor transformado:{bend(mapa,cont2.dict())}")
