Let = input('Escriba una letra: ').lower()


if len(Let) !=1 or not Let.isalpha():

    print('Por favor ingrese una letra: ')
else:
    if Let in "aeiou":
        print(f'La letra {Let} es una vocal')
    else:
        print(f'la letra {Let} es una consonante')

