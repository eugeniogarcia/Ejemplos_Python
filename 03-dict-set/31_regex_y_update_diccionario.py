# 31_regex_y_update_diccionario.py
# Usa regular expresion
# Actualiza un diccionario usando un método no tan optimo
# Cuando una key no existe y accedemos a ella con miDicc["key"] se lanza una excepción. Podemos hacer miDicc.get("key",valor_por_defecto)

import sys
# Suporte a expresiones regulares
import re

WORD_RE = re.compile(r'\w+')

#########################
# diccionario donde guardaremos los resultados
# Es un diccionario normal. Si hacemos index["key"] y "key" no existe se lanza una excepción. Si usamos index.get("key", defecto), en lugar de lanzar una excepción retornaría defecto
#En este ejemplo vemos que para poder actualizar con "seguridad" una key, necesitamos hacer tres acciones
#########################
index = {}

# Abre un archivo
with open(sys.argv[1], encoding='utf-8') as fp:
    # Crea un iterable con los contenidos del archivo, empezando en la posición 1
    for line_no, line in enumerate(fp, 1):
        # Crea un iterable con los resultados de la expresion regular
        for match in WORD_RE.finditer(line):
            # recupera el valor que se ha encontrado que respeta el patron
            word = match.group()
            # recupera la posición en la que se encuentra el valor
            column_no = match.start() + 1
            location = (line_no, column_no)

            #########################
            # # Actualiza el diccionario
            # es un método más rebuscado que el que se muestra en 32_regex_y_update_diccionario.py
            # recupera el valor de la key, y [] en caso de no existir la key
            #########################
            occurrences = index.get(word, [])
            # Añade la nueva ubicación a la lista y actualiza el diccionario
            occurrences.append(location)
            index[word] = occurrences

# Recupera el diccionario ordenado
for word in sorted(index, key=str.upper):
    print(word, index[word])
