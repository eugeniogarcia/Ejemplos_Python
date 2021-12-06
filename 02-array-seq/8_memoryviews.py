from array import array

# Con la memoryview creamos un puntero a una zona de memoria ocupada por un array
octets = array('B', range(6))
# Creamos una vista
m1 = memoryview(octets)

# Veamos el contenido
print(f"m1: {m1.tolist()}")

# Cambiamos la dimensión
m2 = m1.cast('B', [2, 3])
print(f"m2: {m2.tolist()}")

# Otro cambio más
m3 = m1.cast('B', [3, 2])
print(f"m3: {m3.tolist()}")

# Veamos como todos apuntan a la misma memoria
m2[1, 1] = 22
m3[1, 1] = 33

# El contenido ha cambiado
print(f"{octets}")
