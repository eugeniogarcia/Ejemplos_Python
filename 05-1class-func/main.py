from coordinates_3 import Coordenada_basic,Coordenada_typed_namedtuple, Coordenada_dataclass


if __name__ == '__main__':
    #Clase "normal"
    try:
        #No incluye doc y el constructor hay que definirlo explicitamente
        print(f'doc: {Coordenada_basic.__doc__}')
        #Todos los campos que esten tipados se incluyen en annotations
        print(f'Anotaciones: {Coordenada_basic.__annotations__}')
        #lat no esta definido, nos dara una excepción
        print(f'{Coordenada_basic.otro}')
        print(f'{Coordenada_basic.lon}')
        print(f'{Coordenada_basic.lat}')
    except Exception as ex:
        print(f'{ex.__repr__()}')

    try:
        #Incluye doc. El constructor se crea automáticamente con todos los campos tipados
        print(f'doc: {Coordenada_typed_namedtuple.__doc__}')
        #Todos los campos que esten tipados se incluyen en annotations
        print(f'Anotaciones: {Coordenada_basic.__annotations__}')
        #A Todos los campos tipados se les define automaticamente un descriptor, incluso al que no tiene valor
        print(f'{Coordenada_typed_namedtuple.lat} {Coordenada_typed_namedtuple.lon} {Coordenada_typed_namedtuple.otro}')
    except Exception as ex:
        print(f'{ex.__repr__()}')

    try:
        #Incluye doc. El constructor se crea automáticamente con todos los campos tipados
        print(f'doc: {Coordenada_dataclass.__doc__}')
        #Todos los campos que esten tipados se incluyen en annotations
        print(f'Anotaciones: {Coordenada_dataclass.__annotations__}')
        #A Todos los campos tipados se les define automaticamente un descriptor, incluso al que no tiene valor
        print(f'{Coordenada_dataclass.lat} {Coordenada_dataclass.lon} {Coordenada_dataclass.otro}')
    except Exception as ex:
        print(f'{ex.__repr__()}')