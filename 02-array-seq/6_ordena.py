from random import shuffle as baraja

fruits = ['grape', 'raspberry', 'apple', 'banana']
print(f"{fruits}")
print(f"ordena {sorted(fruits)} creando un nuevo objeto inplace {fruits}")
print(f"ordena {sorted(fruits, reverse=True)} creando un nuevo objeto a la inversa {fruits}")
print(f"ordena {sorted(fruits, key=len)} creando un nuevo objeto en base al largo de cada item {fruits}")
print(f"ordena {sorted(fruits, key=len, reverse=True)} creando un nuevo objeto en forma inversa en base al largo de cada item inplace {fruits}")

# Cuando los cambios se hacen inplace, el método retorna None
print(f"shuffle {baraja(fruits)} inplace {fruits}")

# Ordena creando un nuevo objeto
print(f"ordena {fruits.sort()} inplace {fruits}")
