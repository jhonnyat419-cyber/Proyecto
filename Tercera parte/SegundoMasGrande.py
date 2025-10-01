lista = [3, 8, 1, 10, 5, 7]
lista_ord = sorted(set(lista), reverse=True)
if len(lista_ord) >= 2:
    print('El segundo mayor es:', lista_ord[1])
else:
    print('No hay segundo mayor')
