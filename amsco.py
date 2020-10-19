import numpy as np
import string
import codecs

def preprocesar_data(texto):
    tildes = ['á', 'é', 'í', 'ó', 'ú']
    tildes_cambio = ['a', 'e', 'i', 'o', 'u']

    for i in range(len(tildes)):
        texto = texto.replace(tildes[i], tildes_cambio[i])

    tildes = ['Á', 'É', 'Í', 'Ó', 'Ú']
    tildes_cambio = ['A', 'E', 'I', 'O', 'U']

    for i in range(len(tildes)):
        texto = texto.replace(tildes[i], tildes_cambio[i])

    texto = texto.upper()

    texto = (texto.strip().replace(" ", ""))
    translator = str.maketrans('', '', string.punctuation)
    texto = texto.translate(translator)
    texto = texto.replace("…", "")
    texto = texto.replace("¡", "")
    texto = texto.replace("\n", "")
    return texto

diccionario = {}
diccionarioB = {}

def iniciar_diccionario():
    contador = 0
    for i in range(65, 91):
        if i - ord('A') == 14:
            diccionario['Ñ'] = 14
            diccionarioB[14] = 'Ñ'
            contador += 1
        diccionario[chr(i)] = contador
        diccionarioB[contador] = chr(i)
        contador += 1


def guardado_data(texto):
    salida = open("salida.txt", "w")
    salida.write(texto)
    salida.close()


def order_for_pairs(val):
    return val[0]


def getorden_clave(clave):
    numbers = []
    for val in clave:
        numbers.append((diccionario[val], val))

    k = sorted(numbers, key=order_for_pairs)
    v = [0] * len(clave)
    second_clave = list(clave)
    for i in range(len(k)):
        for j in range(len(second_clave)):
            if second_clave[j] == '-':
                continue
            if k[i][1] == second_clave[j]:
                second_clave[j] = '-'
                v[j] = i+1
                break
    return v


def cifrado_AMSCO(texto, clave):
    val = getorden_clave(clave)
    start = 0
    conjunto = []
    paso = True
    while start < len(texto):
        if paso:
            conjunto.append(texto[start: min(start + 1, len(texto))])
            start = start + 1
        else:
            conjunto.append(texto[start: min(start + 2, len(texto))])
            start = start + 2
        paso = not paso

    start = 1
    answer = ""
    while start <= len(clave):
        for i in range(len(clave)):
            if val[i] == start:
                palabra = ""
                for j in range(i, len(conjunto), len(clave)):
                    palabra += conjunto[j]
                answer += palabra
        start += 1
        if start != len(clave)+1:
            answer += " "

    return answer


data = codecs.open("texto_entrada.txt", "r","utf8")
texto = ["", ""]
estado = 0
for frase in data:
    if frase[0] == "#":
        estado += 1
        continue
    texto[estado] += frase.replace("\n", "")


texto[0] = preprocesar_data(texto[0])
iniciar_diccionario()

cifrado = cifrado_AMSCO(texto[0], texto[1])
print("Muestra didáctica")
print(cifrado)
cifrado2 = cifrado.replace(' ','')
print("Muestra final")
print(cifrado2)
guardado_data(str(cifrado))
data.close()
