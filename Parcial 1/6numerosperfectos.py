
n = int(input('Ingresa un número entero positivo: '))

suma_divisores = 0
for i in range(1, n):
    if n % i == 0:
        suma_divisores += i

if suma_divisores == n:
    print(n, 'es un número perfecto.')
else:
    print(n, 'no es un número perfecto.')
