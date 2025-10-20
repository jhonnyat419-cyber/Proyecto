# Ingresar valores de la primera matriz
print('Ingresa los valores de la primera matriz 2x2:')
matriz1 = []
for i in range(2):
    fila = []
    for j in range(2):
        valor = int(input(f'Elemento [{i+1}][{j+1}]: '))
        fila.append(valor)
    matriz1.append(fila)



print('Ingresa los valores de la segunda matriz 2x2:')
matriz2 = []
for i in range(2):
    fila = []
    for j in range(2):
        valor = int(input(f'Elemento [{i+1}][{j+1}]: '))
        fila.append(valor)
    matriz2.append(fila)


matriz_suma = []
for i in range(2):
    fila = []
    for j in range(2):
        fila.append(matriz1[i][j] + matriz2[i][j])
    matriz_suma.append(fila)


print('\nLa matriz resultante de la suma es:')
for fila in matriz_suma:
    print(fila)
