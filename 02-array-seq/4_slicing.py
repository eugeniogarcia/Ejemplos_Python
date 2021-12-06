####################
#Slicing
####################

invoice = """
0.....6.................................40........52...55........
1909  Pimoroni PiBrella                     $17.50    3    $52.50
1489  6mm Tactile Switch x20                 $4.95    2     $9.90
1510  Panavise Jr. - PV-201                 $28.00    1    $28.00
1601  PiTFT Mini Kit 320x240                $34.95    1    $34.95
"""

line_items = invoice.split('\n')[2:]

#Muestra los valores a la inversa de dos en dos
print (line_items[1:6:-2])

#Cuando usamos esta notacion, se crea un slice y el slice es lo que se pasa al operador []. Podemos crear los slices manualmente:
SKU = slice(0, 6)
DESCRIPTION = slice(6, 40)
UNIT_PRICE = slice(40, 52)
QUANTITY =  slice(52, 55)
ITEM_TOTAL = slice(55, None)
#... y usamos __getitems__ para recuperar los valores de los slices
for item in line_items:
    print(item[UNIT_PRICE], item[DESCRIPTION])

#Se puede utilizar un slice para actualizar una lista, pero lo que se pase como argumento tiene que se un iterable:
l = list(range(10))
l[2:5] = [20, 30]