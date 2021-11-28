# Introducción

- `Card = collections.namedtuple('Card', ['rank', 'suit'])`. Se crea una mapped tuple. Esto implementa una clase con el nombre indicado, _Card_ y con los campos que se indican en la lista. Es inmutable:
```py
Card = collections.namedtuple('Card', ['rank', 'suit'])
```

Podemos crear una instancia con:

```py
Card(rank, suit)
```

- Iterable. Al definir la clase con *\__len\__* y *\__getitem\__* estamos creando un iterable:

```pyc
class FrenchDeck:
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]
```

- En el modulo _vector2d_ estamos definiendo el comportamiento de los operandos _+, *, bool y valor absoluto_

## Aplicación de consola

Creamos una aplicación de consola con `click`:

```py
import click

@click.command()
@click.option('--total', default=1, help='Número de saludos.')
@click.option('--nombre', prompt='Nombre',help='La persona a saludar.')
def hello(total, nombre):
    """Programa de ejemplo que saluda a NAME un total de COUNT veces."""
    for x in range(total):
        click.echo(f"Hola {nombre}!")

if __name__ == '__main__':
    hello()
```

- Usamos el paquete `click`
- Anotamos con `@click.command()` el método de entrada para la aplicación de consola
- Anotamos con `@click.options()` los distintos argumentos que usaremos en la función de consola:
  - _prompt_ hará que se nos pregunte por el parametro
  - _default_ establece el valor por defecto caso de no informar ninguno
  - _help_ muestra el mensaje de ayuda asociado al parámetro
  - Los parametros de la función coinciden con los nombres de los parametros

## Doctest

Doctest permite definir casos de prueba a ejecutar con el terminal de python. El módulo que hace posible esto es parte de python. Podemos usar esta funcionalidad de dos maneras:
- en un módulo py podemos incluir tests como parte de los mensajes de ayuda
- en un archivo de texto separado

### Módulo py

```ps
python ej_doctest.py 
```

Ejecutara todos los tests. Si queremos ver la ejecución de los tests haremos:

```ps
python ej_doctest.py -v

Trying:
    factorial(5)
Expecting:
    120
ok
Trying:
```

### Documento de texto

```ps
python -m doctest -v frenchdeck.doctest
```

### Como funciona

Todo lo que se indica con el simbolo _>>>_ se ejecuta como parte del test, y el resultado se compara con lo que se indique a continuación en el archivo. Si se trata de un módulo de python, estas instrucciones se incluyen en los comentarios del código.

Si en los resultados se obtuviera un número largo de valores, se pueden indicar apenas unos pocos y marcar con una elipsis que hay más datos. A _doctest_ hay que avisarle de esto:

```txt
>>> for card in deck:  # doctest: +ELLIPSIS
...   print(card)
Card(rank='2', suit='spades')
Card(rank='3', suit='spades')
Card(rank='4', suit='spades')
```

Para avisar s usa la directiva _# doctest: +ELLIPSIS_
