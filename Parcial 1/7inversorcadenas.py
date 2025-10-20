# Pedir una palabra o frase al usuario
date = input('Ingresa una palabra o frase: ')


invertida = ''
for letra in date:
    invertida = letra + invertida

print('Versión invertida:', invertida)
