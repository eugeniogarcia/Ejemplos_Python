from array import array
import math

class Vector2d:
    typecode = 'd'

    #Para que Vector2d sea inmutable y podamos usarlo en sets, keys de dicccionarios, etc. tenemos que implementar __hash__ y hacer que los miembros sean inmutables. Hacemos pues que x e y sean privadas, y definimos dos propiedades para acceder a ellas - getter
    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    #Con __iter__ conseguimos que se recupere una tupla, y que por lo tanto se pueda desestructurar el objeto
    def __iter__(self):
        return (i for i in (self.x, self.y))

    #representacion para debuggear
    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)

    #representacion para ususario
    def __str__(self):
        return str(tuple(self))

    #para soportar el formateo como bytes
    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(array(self.typecode, self)))

    #para implementar ==
    def __eq__(self, other):
        return tuple(self) == tuple(other)

    #El modulo del objeto. Cuando usamos abs se emplea este método
    def __abs__(self):
        return math.hypot(self.x, self.y)

    #Puede usarse en condiciones booleanas
    def __bool__(self):
        return bool(abs(self))

    def angle(self):
        return math.atan2(self.y, self.x)

    #Proporcionamos soporte para usar format con nuestro tipo
    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:
            coords = self
            outer_fmt = '({}, {})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)

    #Implementa un método de clase, estático. A diferetencia de cuando anotamos el método con @staticmethod, el primer argumento hace referencia a la clase, al tipo. En este ejemplo creamos una instancia de la clase. Con @staticmethod no existe este primer argumento
    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)
