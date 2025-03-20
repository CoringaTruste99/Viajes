import os  # Importamos el módulo 'os' para manejar rutas de archivos y operaciones del sistema.
import pandas as pd  # Importamos la librería 'pandas', que nos permite trabajar con estructuras de datos como DataFrames.

# Obtener la ruta absoluta del directorio donde está el script actual (`conn.py` en este caso)
base_dir = os.path.dirname(os.path.abspath(__file__))  
# `os.path.abspath(__file__)` obtiene la ruta absoluta del script actual.
# `os.path.dirname(...)` extrae el directorio donde está ubicado el script.

# Construimos la ruta al archivo `viajes.csv` que se encuentra en la carpeta 'data', un nivel arriba del directorio actual
filename = os.path.join(base_dir, "..", "data", "viajes.csv")  
# `os.path.join(...)` une los elementos de la ruta de manera compatible con el sistema operativo.
# ".." indica que subimos un nivel en la estructura de directorios desde `base_dir`.
# `"data/viajes.csv"` representa la carpeta `data` y el archivo `viajes.csv` dentro de ella.

def lecture_data():
    """
    Función para leer el archivo CSV y devolver un DataFrame de pandas.
    """
    df = pd.read_csv(filename)  # Utilizamos `pd.read_csv()` para leer el archivo CSV y almacenarlo en un DataFrame.
    return df  # Devolvemos el DataFrame con los datos del archivo CSV.

lecture_data()  # Llamamos a la función para ejecutar la lectura del archivo y obtener los datos.
