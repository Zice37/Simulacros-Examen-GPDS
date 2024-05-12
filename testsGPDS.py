#!/usr/bin/env python3
import sys
from PyPDF2 import PdfReader
import re
import random
import textwrap
import math
import argparse     # Leer parametros de ejecución

RESPUESTAS_VALIDAS = ["A","B","C","D","","S"]

def calcular_nota(respuestas_totales, respuestas_correctas, respuestas_incorrectas):
    if respuestas_totales <= 0:
        return 0
    nota = (respuestas_correctas - math.floor(respuestas_incorrectas / 3)) / respuestas_totales * 10
    return nota

def mostrar_nota(totales, correctas, falladas):
    print("Correctas: ",correctas)
    print("Falladas: ",falladas)
    print("Blanco: ",totales-correctas-falladas)

    print("Totales: ",totales)
    print("Nota: ", calcular_nota(totales, correctas, falladas))

def leer_pdf(args):
    correctas = 0
    totales = 0
    falladas = 0
    wrap = textwrap.TextWrapper(width=80)
    try:
        with open(args.filename, 'rb') as archivo_pdf:
            lector_pdf = PdfReader(archivo_pdf)
            num_paginas = len(lector_pdf.pages)

            patron = r"Pregunta número:\s*(\d+)\s*(.*)\s*A:\s*(.*?)\s*B:\s*(.*?)\s*C:\s*(.*?)\s*D:\s*(.*?)\s*Respuesta correcta:\s*([A-D])"

            paginas = list(range(num_paginas))

            # Mezclar la lista para obtener el orden aleatorio
            random.shuffle(paginas)
            for pagina_num in paginas:
                pagina = lector_pdf.pages[pagina_num]
                texto = pagina.extract_text()

                match = re.search(patron, texto, re.DOTALL)

                if args.numeropreguntas != None:
                    if args.numeropreguntas <= totales:
                        break

                if match:
                    #pregunta_numero = match.group(1).replace("\n", " ")
                    pregunta = wrap.fill( match.group(2).replace("\n", " ")  )
                    respuesta_b = wrap.fill( match.group(4).replace("\n", " ") )
                    respuesta_a = wrap.fill( match.group(3).replace("\n", " ") )
                    respuesta_c = wrap.fill( match.group(5).replace("\n", " ") )
                    respuesta_d = wrap.fill( match.group(6).replace("\n", " ") )
                    respuesta_correcta = match.group(7).replace("\n", " ")

                    totales+=1

                    print(f"Pregunta número: {totales}")
                    print(pregunta)
                    print()
                    print(f"A: {respuesta_a}\n")
                    print(f"B: {respuesta_b}\n")
                    print(f"C: {respuesta_c}\n")
                    print(f"D: {respuesta_d}\n")
                    entrada = input("Introduce tu respuesta:").capitalize()
                    while entrada not in RESPUESTAS_VALIDAS:
                        print("\tRespuesta no comprendida")
                        mostrar_nota(totales-1, correctas, falladas)
                        entrada = input("Introduce tu respuesta:").capitalize()
                    if entrada == respuesta_correcta:
                        correctas+=1
                        print("\tAcierto registrado")
                    elif entrada == "S":
                        totales-=1
                        print("\tSalto de pregunta registrado")
                    elif entrada != "":
                        falladas+=1
                        print("\tFallo registrado")
                    else:
                        print("\tBlanco registrado")

                    print(f"Respuesta correcta: {respuesta_correcta}\n")
                else:
                    print(f"No se encontró un patrón válido en la página {pagina_num + 1}\n")
            return totales, correctas, falladas
    except FileNotFoundError:
        print("El archivo no existe.")
    except KeyboardInterrupt:
        print("\n\tFinalización prematura")
        print(f"Respuesta correcta: {respuesta_correcta}\n")

        totales-=1  #asumimos que si cierra por teclado no ha respondido a la pregunta
        return totales, correctas, falladas
    except Exception as e:
        print(f"Error: {e}")
    return totales, correctas, falladas

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--numeropreguntas", help="Número de preguntas máxima (si no se han excedido las que haya en el documento)", type=int)
    parser.add_argument("filename", help="Archivo de preguntas PDF")
    args = parser.parse_args()

    totales, correctas, falladas = leer_pdf(args)
    print()
    mostrar_nota(totales, correctas, falladas)
