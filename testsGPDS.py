#!/usr/bin/env python3
import sys
from PyPDF2 import PdfReader
import re
import random

def calcular_nota(respuestas_totales, respuestas_correctas, respuestas_incorrectas):
    nota = (respuestas_correctas - (respuestas_incorrectas / 3)) / respuestas_totales * 10
    return nota

def leer_pdf(nombre_archivo):
    correctas = 0
    totales = 0
    falladas = 0
    try:
        with open(nombre_archivo, 'rb') as archivo_pdf:
            lector_pdf = PdfReader(archivo_pdf)
            num_paginas = len(lector_pdf.pages)

            patron = r"Pregunta número:\s*(\d+)\s*(.*)\s*A:\s*(.*?)\s*B:\s*(.*?)\s*C:\s*(.*?)\s*D:\s*(.*?)\s*Respuesta correcta:\s*([A-D])"

            paginas = list(range(num_paginas))

            # Mezclar la lista para obtener el orden aleatorio
            random.shuffle(paginas)
            cont=1
            for pagina_num in paginas:
                pagina = lector_pdf.pages[pagina_num]
                texto = pagina.extract_text()

                match = re.search(patron, texto, re.DOTALL)
                
                if match:
                    #pregunta_numero = match.group(1).replace("\n", " ")
                    pregunta = match.group(2).replace("\n", " ")
                    respuesta_b = match.group(4).replace("\n", " ")
                    respuesta_a = match.group(3).replace("\n", " ")
                    respuesta_c = match.group(5).replace("\n", " ")
                    respuesta_d = match.group(6).replace("\n", " ")
                    respuesta_correcta = match.group(7).replace("\n", " ")

                    totales+=1

                    print(f"Pregunta número: {totales}")
                    print(pregunta)
                    print(f"A: {respuesta_a}")
                    print(f"B: {respuesta_b}")
                    print(f"C: {respuesta_c}")
                    print(f"D: {respuesta_d}")
                    entrada = input("Introduce tu respuesta:")
                    print(f"Respuesta correcta: {respuesta_correcta}\n")
                    if entrada.capitalize() == respuesta_correcta:
                        correctas+=1
                    elif entrada != "":
                        falladas+=1
                               
                else:
                    print(f"No se encontró un patrón válido en la página {pagina_num + 1}\n")
            return totales, correctas, falladas
    except FileNotFoundError:
        print("El archivo no existe.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__": 

    if len(sys.argv) != 2:
        print("Uso: python3 main.py fichero.pdf")
        sys.exit(1)
        
    totales, correctas, falladas = leer_pdf(sys.argv[1])
    print("Correctas: ",correctas)
    print("Falladas: ",falladas)
    print("Blanco: ",totales-correctas-falladas)

    print("Totales: ",totales)
    print("Nota: ", calcular_nota(totales, correctas, falladas))
