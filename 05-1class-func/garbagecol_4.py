import weakref

#Creamos un diccionario
s1 = {1, 2, 3}
#Una referencia
s2 = s1

def bye():
    print('...like tears in the rain.')

#Weak Reference. Seguimos a s1
ender = weakref.finalize(s1, bye)

#Nos dice si la s1 sigue activa
print (f'Sigue viva? {ender.alive}')

#Borramos la variable. Como s2 sigue apuntando a esta objeto, el weakref no se pierde
del s1
print (f'Sigue viva? {ender.alive}')

#Ahora se apunta a otro lugar s2, así que la referencia se pierde
s2 = 'spam'
print (f'Sigue viva? {ender.alive}')
