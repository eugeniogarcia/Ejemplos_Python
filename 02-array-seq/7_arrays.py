from array import array
from random import random

# Crea array de decimales
floats = array('d', (random() for i in range(10**7)))
print(f"{floats[-1]}")

# Podemos escribir el array a un archivo
fp = open('floats.bin', 'wb')
floats.tofile(fp)
fp.close()

# Lo podemos leer del archivo
floats2 = array('d')
fp = open('floats.bin', 'rb')
floats2.fromfile(fp, 10**7)
fp.close()

# Veamos lo que hemos leido
print(f"{floats2[-1]}")
print(f"¿Son identicos?: {floats2 == floats}")
