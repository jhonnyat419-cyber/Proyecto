frase = input("Escriba una frase: ")
palabras = frase.split()
mas_larga = ""

for p in palabras:
    if len(p) > len(mas_larga):
        mas_larga = p

print("La palabra más larga es:", mas_larga)
print(f"tiene {len(mas_larga)} letras")