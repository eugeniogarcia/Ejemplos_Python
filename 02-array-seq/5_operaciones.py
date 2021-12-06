####################
# USo de + y * con secuencias
####################

# En ambos casos con estos operandos se crean un objeto nuevo
# Concatena
a = [1, 2, 3]
b = [4, 5, 6]
c = a+b
print(c)

# Crear varias copias de la misma secuencia
d = a * 3
print(d)

weird_board = [['_'] * 3] * 3
print(weird_board)
weird_board[1][2] = 'O'
print(f"comportamiento extraño {weird_board}")

board = [['_'] * 3 for _ in range(3)]
print(board)
board[1][2] = 'O'
print(f"comportamiento normal {board}")

# Los objetos que incluyen __iadd__ permiten soportar la actualización inplace. Cuando __iadd__ no esta implementada python hace un failback a __add__ y el resultado de la operación es un nuevo objeto. Las listas incluyen __iadd__ así que se actualiza el objeto inplace. Las tuplas no implementan __iadd__
l = [1, 2, 3]
print(f"{l} id: {id(l)}")
l *= 3
print(f"{l} tiene el mismo id porque es el mismo objeto: {id(l)}")

t = (1, 2, 3)
print(f"{t} id: {id(t)}")
t *= 3
print(f"{t} tiene otro id porque es un nuevo objeto: {id(t)}")
