palabra = input('Ingrese una palabra: ').lower()
if palabra == palabra[::-1]:
    print('Es palíndromo')
else:
    print('No es palíndromo')
