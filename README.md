# -S5-Simulador-de-editor-con-historial-de-acciones-usando-pilas
INSTRUCCIONES DE EJECUCION DEL SISTEMA:
1. Requisitos Previos
Python 3.x: Asegúrate de tener instalado Python en tu computadora. Puedes verificarlo abriendo una terminal o CMD y escribiendo python --version.

Librería Tkinter: Es la biblioteca para interfaces gráficas. Normalmente viene instalada por defecto con Python. Si usas Linux (como Ubuntu), es posible que necesites instalarla manualmente con:
sudo apt-get install python3-tk, 

2. Pasos para la Ejecución
Guardar el archivo:
Copia el código proporcionado y guárdalo en una carpeta local con el nombre editor_texto.py.

Abrir la Terminal o Consola:
Navega hasta la carpeta donde guardaste el archivo.

Ejecutar el script:
Escribe el siguiente comando y presiona Enter:

Bash
python editor_texto.py
3. Qué esperar al ejecutarlo
Al iniciar el programa, sucederán dos cosas en orden:

Fase de Pruebas (Consola): El código ejecutará primero la función run_tests(). Si todo está correcto, verás el mensaje "Pruebas pasadas correctamente" en tu terminal.

Interfaz Gráfica: Inmediatamente después, se abrirá una ventana titulada "Editor Profesional Pro".

4. Uso de las Funciones
Dentro de la ventana, podrás interactuar con los siguientes elementos:

Escribir: Abre un cuadro de diálogo para agregar texto. El sistema añade un espacio automáticamente si ya hay contenido.

Borrar: Solicita un número para eliminar esa cantidad de caracteres desde el final hacia atrás.

Deshacer/Rehacer: Utiliza las estructuras de datos tipo Stack para revertir o repetir acciones.

Ver Historial: Muestra una lista de todas las acciones realizadas (escritura, borrado, undo, redo) en orden inverso (la más reciente primero).
