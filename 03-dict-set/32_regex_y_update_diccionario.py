# 32_regex_y_update_diccionario.py
# Usa regular expresion
# Actualiza un diccionario usando un método más optimo
# Cuando una key no existe y accedemos a ella con miDicc["key"] se lanza una excepción. Si hacemos miDicc.setdefault("key",valor_por_defecto) recuperamos una referencia al valor que podemos usar para actualizarlo en una sola instrucción

import sys
# Suporte a expresiones regulares
import re

WORD_RE = re.compile(r'\w+')

# diccionario donde guardaremos los resultados
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
            column_no = match.start()+1
            location = (line_no, column_no)

            # Actualiza el diccionario
            index.setdefault(word, []).append(location)

# Recupera el diccionario ordenado
for word in sorted(index, key=str.upper):
    print(word, index[word])
