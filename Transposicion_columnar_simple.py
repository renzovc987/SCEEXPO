import numpy as np
import string


def preprocesar_data(texto):
    tildes = ['á', 'é', 'í', 'ó', 'ú']
    tildes_cambio = ['a', 'e', 'i', 'o', 'u']

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
    contador = 1
    for i in range(65, 91):
        if i - ord('A') == 15:
            diccionario['Ñ'] = 15
            diccionarioB[15] = 'Ñ'
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
    for k in clave:
        numbers.append((diccionario[k], k))

    numbers = sorted(numbers, key=order_for_pairs)
    answer_clean = []
    for (j, k) in numbers:
        answer_clean.append(k)
    return answer_clean


def descifrado_columna_simple(texto, clave):
    # lo primero es ordenar la clave acorde a su valor en el alfabeta empezando en 1
    val = getorden_clave(clave)
    # valores utiles para el trabajo del algoritmo,  np.ceil aproxima a techo
    longitud_clave = len(clave)
    salto = int(np.ceil(len(texto) / longitud_clave))
    # conversión a  lista, ya que no puedo iterar en un string
    clave_evaluar = list(clave)
    texto = list(texto)
    # matriz de respuesta (equivalente a la que se encuentra en el pdf)
    matriz_answer = np.array([['-']*longitud_clave] * salto)
    # dado que puede haber el caso que la longitud texto no sea divisible con la longitud de la clave
    diferencia = len(clave) * salto - len(texto)
    # valor para moverse por el texto codificado
    start = 0
    # El primer for avanza  en el array con las letras de la clave ordenadas
    for i in range(len(val)):
        # El segundo for avanza por el array con las letras de la clave desordenadas

        for j in range(len(clave_evaluar)):
            # este valor es un auxiiar dado que puede existir varios repeticiones de una letra
            if clave_evaluar[j] == '-':
                continue
            # En caso de encontrar el valor desordenado equivalente al valor ordenado
            if val[i] == clave_evaluar[j]:
                # Se bloquea el valor ya encontrado
                clave_evaluar[j] = '-'
                # en caso de exista elementos no este llena de elementos en la última fila de la matriz

                if diferencia > 0:
                    # verificar si se usara toda la columna, o el último valor es basura
                    if j % longitud_clave <= diferencia:
                        matriz_answer[:, j] = texto[start:start+salto]
                        start += salto
                    else:
                        matriz_answer[0:-1, j] = texto[start:start + salto-1]
                        start += salto-1
                # si no hay este problema
                else:
                    matriz_answer[:, j] = texto[start:start + salto]
                    start += salto
                break

    answer = ""
    for i in range(salto):
        for j in range(longitud_clave):
            if matriz_answer[i, j] == '-':
                break
            answer += matriz_answer[i, j]
    return answer


data = open("texto_entrada.txt", "r")
texto = ["", ""]
estado = 0

for frase in data:
    if frase[0] == "#":
        estado += 1
        continue
    texto[estado] += frase.replace("\n", "")


texto[0] = preprocesar_data(texto[0])
iniciar_diccionario()

cifrado = descifrado_columna_simple(texto[0], texto[1])
# dic_data, text_data = frecuencias(cifrado)
print(cifrado)
guardado_data(cifrado)
data.close()