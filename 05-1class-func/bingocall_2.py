import random

class BingoCage:

    def __init__(self, items):
        #Crea una nueva copia -swallow copy - de items. Así no lo comparten todas las instancias
        self._items = list(items)
        #Shuffle in place de la lista 
        random.shuffle(self._items)

    # extrae un valor de la lista
    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')  # <4>

    # Hace un callable de esta clase
    def __call__(self):  # <5>
        return self.pick()

b1=BingoCage(['eugenio','nico','pupa','nani','clara','vera'])

print(b1.pick())

print(b1())
