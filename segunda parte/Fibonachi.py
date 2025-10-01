a, b = 0,1
print('Los primeros numeros de fibonacci son: ')
for _ in range(20):
    print(a, end=' ')
    a, b= b, a + b
print()
