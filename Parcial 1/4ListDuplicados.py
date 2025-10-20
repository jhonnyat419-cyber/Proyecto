date = input('Ingrese una lista de datos separados por comas: ')

lista = date.split(',')

New_list = []

for elemento in lista:
    if elemento not in New_list:
        New_list.append(elemento)


print(f'lista sin duplicados: {New_list}')