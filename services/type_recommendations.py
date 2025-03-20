import os  # Importa el módulo 'os' que proporciona una forma de interactuar con el sistema operativo, como trabajar con rutas de archivos.
import pandas as pd  # Importa la librería 'pandas' para manipulación y análisis de datos en estructuras tabulares como DataFrames.

# Obtener la ruta absoluta del directorio donde está este archivo ('conn.py').
# __file__ es una variable especial que almacena la ruta del archivo Python que se está ejecutando.
base_dir = os.path.dirname(os.path.abspath(__file__))  

# Aquí se construye la ruta completa hacia el archivo CSV 'Recomendations_for_types.csv', 
# subiendo un nivel (a la carpeta raíz del proyecto) y luego entrando a la carpeta 'data'.
filename = os.path.join(base_dir, "..", "data", "Recomendations_for_types.csv")  

def lecture_type_recommendations():
    """
    Esta función lee el archivo CSV que contiene las recomendaciones de tipo y las carga en un DataFrame de pandas.
    Retorna el DataFrame con los datos cargados.
    """
    df = pd.read_csv(filename)  # Usa pandas para leer el archivo CSV y cargarlo en un DataFrame.
    return df  # Retorna el DataFrame con los datos del archivo.

# Llama a la función 'lecture_type_recommendations' para cargar los datos.
# Esta llamada no hace nada con los datos aún, solo ejecuta la función para cargar el DataFrame.
lecture_type_recommendations()  