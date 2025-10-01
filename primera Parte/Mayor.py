num1 = int(input('ingrese el primer numero '))
num2 = int(input('ingrese el segundo numero '))
num3 = int(input('ingrese el tercer numero '))


if num1 >= num2 and num1 >= num3:
    mayor = num1
elif num2 >= num1 and num2 >= num3:
    mayor = num2
else:
    mayor = num3


print('El numero mayot es:',mayor)