"""Taller evaluable"""

# pylint: disable=broad-exception-raised

import fileinput
import glob
import os
import os.path
import time
from itertools import groupby


#
# Escriba la funcion que  genere n copias de los archivos de texto en la
# carpeta files/raw en la carpeta files/input. El nombre de los archivos
# generados debe ser el mismo que el de los archivos originales, pero con
# un sufijo que indique el número de copia. Por ejemplo, si el archivo
# original se llama text0.txt, el archivo generado se llamará text0_1.txt,
# text0_2.txt, etc.
#
def copy_raw_files_to_input_folder(n):
    """Funcion copy_files"""
    raw_files = glob.glob("files/raw/*.txt")
    os.makedirs("files/input", exist_ok=True)

    for file_path in raw_files:
        base_name = os.path.basename(file_path).replace('.txt', '')
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        for i in range(1, n + 1):
            new_name = f"{base_name}_{i}.txt"
            new_path = os.path.join("files/input", new_name)
            with open(new_path, "w", encoding="utf-8") as new_file:
                new_file.write(content)


#
# Escriba la función load_input que recive como parámetro un folder y retorna
# una lista de tuplas donde el primer elemento de cada tupla es el nombre del
# archivo y el segundo es una línea del archivo. La función convierte a tuplas
# todas las lineas de cada uno de los archivos. La función es genérica y debe
# leer todos los archivos de folder entregado como parámetro.
#
def load_input(input_directory):
    """Funcion load_input"""
    result = []
    files = glob.glob(os.path.join(input_directory, "*.txt"))
    for file_path in files:
        file_name = os.path.basename(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                cleaned_line = line.strip()
                if cleaned_line:
                    result.append((file_name, cleaned_line))
    return result


#
# Escriba la función line_preprocessing que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). Esta función
# realiza el preprocesamiento de las líneas de texto,
#
def line_preprocessing(sequence):
    """Line Preprocessing"""
    result = []
    for filename, line in sequence:
        # Eliminar signos de puntuación y convertir a minúsculas
        words = ''.join(c if c.isalnum() else ' ' for c in line).split()
        for word in words:
            result.append((word.lower(), 1))
    return result


#
# Escriba una función llamada maper que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). En este caso,
# la clave es cada palabra y el valor es 1, puesto que se está realizando un
# conteo.
#
def mapper(sequence):
    """Mapper"""
    return sequence  # Ya está en formato (palabra, 1)


#
# Escriba la función shuffle_and_sort que recibe la lista de tuplas entregada
# por el mapper, y retorna una lista con el mismo contenido ordenado por la
# clave.
#
def shuffle_and_sort(sequence):
    """Shuffle and Sort"""
    return sorted(sequence, key=lambda x: x[0])


#
# Escriba la función reducer, la cual recibe el resultado de shuffle_and_sort y
# reduce los valores asociados a cada clave sumandolos. Como resultado, por
# ejemplo, la reducción indica cuantas veces aparece la palabra analytics en el
# texto.
#
def reducer(sequence):
    """Reducer"""
    result = []
    for key, group in groupby(sequence, key=lambda x: x[0]):
        total = sum(count for _, count in group)
        result.append((key, total))
    return result


#
# Escriba la función create_ouptput_directory que recibe un nombre de
# directorio y lo crea. Si el directorio existe, lo borra
#
def create_ouptput_directory(output_directory):
    """Create Output Directory"""
    if os.path.exists(output_directory):
        for file in os.listdir(output_directory):
            os.remove(os.path.join(output_directory, file))
    else:
        os.makedirs(output_directory)


#
# Escriba la función save_output, la cual almacena en un archivo de texto
# llamado part-00000 el resultado del reducer. El archivo debe ser guardado en
# el directorio entregado como parámetro, y que se creo en el paso anterior.
# Adicionalmente, el archivo debe contener una tupla por línea, donde el primer
# elemento es la clave y el segundo el valor. Los elementos de la tupla están
# separados por un tabulador.
#
def save_output(output_directory, sequence):
    """Save Output"""
    output_file = os.path.join(output_directory, "part-00000")
    with open(output_file, "w", encoding="utf-8") as f:
        for key, value in sequence:
            f.write(f"{key}\t{value}\n")


#
# La siguiente función crea un archivo llamado _SUCCESS en el directorio
# entregado como parámetro.
#
def create_marker(output_directory):
    """Create Marker"""
    marker_path = os.path.join(output_directory, "_SUCCESS")
    with open(marker_path, "w") as f:
        f.write("")


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run_job(input_directory, output_directory):
    """Job"""
    data = load_input(input_directory)
    preprocessed = line_preprocessing(data)
    mapped = mapper(preprocessed)
    sorted_data = shuffle_and_sort(mapped)
    reduced = reducer(sorted_data)
    create_ouptput_directory(output_directory)
    save_output(output_directory, reduced)
    create_marker(output_directory)


if __name__ == "__main__":

    copy_raw_files_to_input_folder(n=1000)

    start_time = time.time()

    run_job(
        "files/input",
        "files/output",
    )

    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")