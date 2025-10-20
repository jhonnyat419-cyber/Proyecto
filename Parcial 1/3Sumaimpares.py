num = int(input('Digite el numero hasta donde se realizara la suma: '))

suma = 0

for i in range(1,num+1):
    if i % 2 !=0:
        suma +=i


print('la suma de los impares es: ',suma)