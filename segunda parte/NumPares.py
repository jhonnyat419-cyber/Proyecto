
num = int(input('Ingrese un número: '))

print(f'Los números pares desde 1 hasta {num} son:')

for i in range(1, num + 1):
    if i % 2 == 0:
        print(i)
