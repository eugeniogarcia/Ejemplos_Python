# 32_regex_y_update_diccionario.py
# Usa regular expresion
# Actualiza un diccionario usando defaultdict
# El constructor de defaultdict nos permite indicar un callable. Este callable se invocará para generar un valor por defecto cuando se este accediendo a una key que no exista.

import sys
import collections
# Suporte a expresiones regulares
import re

WORD_RE = re.compile(r'\w+')

#########################
# Usamos defaultdict en lugar de un diccionario como hemos hecho en los otros ejemplos
# La actualización es mucho más simple
#########################
index = collections.defaultdict(list)

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
            # Actualiza el diccionario directamente. Si la clave no existe en lugar de dar un error se llama al callable para crearla, y se devuelve la referencia
            # Si word no existiera, se llama al callable list - segun indicamos en el constructor de index - y devuelve UNA REFERENCIA al valor, esto es, a la lista, que podemos actualizar
            #########################
            index[word].append(location)

# Recupera el diccionario ordenado
for word in sorted(index, key=str.upper):
    print(word, index[word])
