####################
#unpacking
####################

#Se puede usar unpacking tanto al pasar argumentos a funciones, como al recibir respuestas de funciones
#Con el * indicamos que queremos desenpaquetar en rest
a, b, *rest = range(5)
print(f"{a}, {b}, {rest}")

#Indicamos que lo que pasemos a partir del quinto argumento lo empaquetaremos en rest
def fun(a, b, c, d, *rest):
    print(f"{a}, {b}, {c}, {d}, {rest}")
    return a, b, c, d, rest

#Indicamos que desempaquetamos [1 2], y range(4,7). Una vez desempaquetados se llama a la función, y se empaquetan los argumentos en rest como hemos definido en la función
a,_,c,*rest=fun(*[1, 2], 3, *range(4, 7))
print(f"{a}, {c}, {rest}")
