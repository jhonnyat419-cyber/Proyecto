Pal = input('Ingrese una palabra: ').lower()
Voc = 'aeiou'
Cont = sum(1 for letra in Pal if letra in Voc)
print('La palabra tiene', Cont, 'vocal(es)')