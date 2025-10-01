num = int(input('Ingrese un numero: '))

print('La tabla de multiplicar del numero {num} es:')

for i in range(1,11):
    res = num * i

    print(f'{num} * {i} = {res}')  