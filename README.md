# Simulacros-Examen-GPDS
Este es un pequeño código para prácticar los tests de SIDRA de GPDS más cómodamente.

## Uso
Esta pensado para leer los ficheros subidos por los profesores de la asignatura.
Aun así, se puede cambiar fácilmente la expresión regular con la que se buscan preguntas de modo que funcione con más PDFs.

Notas para el uso del programa:
- Al terminar de analizar todas las páginas del PDF se muestran un resumen del simulacro con el total de preguntas realizadas, la nota, etc.
- Para dejar en blanco una respuesta simplemente pulsa Enter sin escribir nada.
- En caso de querer terminar el simulacro antes de tiempo, con Ctrl+C se detienen las preguntas y muestra el resumen del simulacro. 
- Con el argumento -n, puedes especificar un número máximo de preguntas a realizar en el test. (Nota: si no hay más preguntas en el pdf, se acaba de todos modos)
- Puedes responder a una pregunta con una 'S' para saltarla y que no cuente en el total de preguntas. Útil cuando no quieres que cuente una pregunta repetida que ya conocías la respuesta.


# Dependecias
Si os da algun error de dependecias al ejecutarlo, podeis probar a instalar:
- PyPDF2
- regex
- textwrap

mediante el comando: pip install xxx
