num = int(input('Digite un numero: '))

Fac = 1

if num<0:
    print('la factorial no esta definida para numeros negativos')
else:
    for i in range(1, num + 1):
        Fac *= i
    print(f'la factorial del numero {num} es: {Fac}')