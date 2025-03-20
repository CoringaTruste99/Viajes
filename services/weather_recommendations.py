import os  # Importa el módulo 'os' para interactuar con el sistema operativo, como manipular rutas de archivos.
import pandas as pd  # Importa 'pandas' para manipulación y análisis de datos en estructuras tabulares, como DataFrames.

# Obtener la ruta absoluta del directorio donde está este archivo ('conn.py').
# __file__ es una variable especial que contiene la ruta del archivo Python que se está ejecutando.
base_dir = os.path.dirname(os.path.abspath(__file__))  

# Construir la ruta completa del archivo CSV 'Recomendations_for_weathers.csv',
# subiendo un nivel (a la carpeta raíz del proyecto) y luego accediendo a la carpeta 'data'.
filename = os.path.join(base_dir, "..", "data", "Recomendations_for_weathers.csv")  # Subir un nivel

def lecture_weather_recommendations():
    """
    Esta función lee el archivo CSV que contiene las recomendaciones basadas en el clima y las carga en un DataFrame de pandas.
    Retorna el DataFrame con los datos cargados.
    """
    df = pd.read_csv(filename)  # Usa pandas para leer el archivo CSV y cargarlo en un DataFrame.
    return df  # Retorna el DataFrame con los datos del archivo.

# Llama a la función 'lecture_weather_recommendations' para cargar los datos del archivo CSV en un DataFrame.
# Esta llamada ejecuta la función, pero no hace nada con el DataFrame cargado, solo lo lee.
lecture_weather_recommendations()