# Importación de módulos necesarios
import re  # Para trabajar con expresiones regulares y buscar patrones en strings.
from services.conn import lecture_data  # Importa la función que obtiene datos (posiblemente de una BD o CSV).
from services.type_recommendations import lecture_type_recommendations  # Importa función que devuelve recomendaciones basadas en el tipo de destino.
from services.weather_recommendations import lecture_weather_recommendations  # Importa función que devuelve recomendaciones basadas en el clima.
import geopy.distance  # Para calcular la distancia entre dos coordenadas geográficas.
import requests  # Para hacer solicitudes HTTP (usado para obtener la ubicación del usuario).
import pandas as pd  # Para manipulación de datos con DataFrames.
import folium  # Para generar mapas interactivos en HTML.
import random  # Para seleccionar elementos aleatorios de listas.

class Manipulate:  # Define la clase que agrupará los métodos de manipulación de datos
    
    def __init__(self):
        self.data = lecture_data()  # Carga los datos al instanciar la clase.

    @staticmethod
    def get_geolocation():
        """
        Obtiene la ubicación del usuario a partir de la API de ipinfo.io.
        Devuelve una tupla con la latitud y longitud en formato float.
        """
        response = requests.get('http://ipinfo.io/json')  # Realiza una solicitud HTTP a la API.
        location = response.json().get("loc", "No location found").split(",")  # Extrae la latitud y longitud.
        return float(location[0]), float(location[1])  # Convierte los valores en flotantes y los retorna.

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """
        Calcula la distancia en metros entre dos puntos geográficos dados.
        Si la distancia es mayor o igual a 1000 metros, la convierte a kilómetros.
        """
        distance = geopy.distance.distance((lat1, lon1), (lat2, lon2)).m  # Calcula la distancia en metros.
        if distance >= 1000:
            return {"value": round(distance / 1000, 2), "unit": "km"}  # Si es mayor a 1000m, convierte a km.
        return {"value": round(distance, 2), "unit": "m"}  # Si es menor, devuelve la distancia en metros.

    @staticmethod
    def filters(selected_type, selected_weather, budget):
        """
        Filtra los destinos en función del tipo de destino, el clima y el presupuesto.
        Retorna un DataFrame con los resultados filtrados y una lista de coordenadas de los destinos encontrados.
        """
        df = lecture_data()  # Carga los datos en un DataFrame.

        if not selected_type or not selected_weather:
            return pd.DataFrame(), []  # Si no se selecciona tipo o clima, devuelve estructuras vacías.

        # Construcción del patrón de búsqueda para el tipo de destino (puede ser lista o string).
        pattern_type = '|'.join([re.escape(t) for t in selected_type]) if isinstance(selected_type, list) else re.escape(selected_type)

        # Construcción del patrón de búsqueda para el clima.
        pattern_weather = '|'.join([f'({re.escape(weather)})' for weather in selected_weather])

        # Filtrado del DataFrame usando coincidencias parciales en "Type" y "Weather" y verificando el costo.
        filtered_df = df[
            df['Type'].str.contains(pattern_type, case=False, na=False) &  # Verifica que el tipo coincida.
            df['Weather'].str.contains(pattern_weather, case=False, na=False) &  # Verifica que el clima coincida.
            (df['Cost'] <= float(budget))  # Verifica que el costo no supere el presupuesto.
        ]

        # Extrae las coordenadas de los destinos filtrados.
        locations = [(float(row['Lat']), float(row['Long'])) for _, row in filtered_df.iterrows()]

        return filtered_df, locations  # Retorna los datos filtrados y las ubicaciones.

    @staticmethod
    def generate_map_for_location(lat, lon, map_index):
        """
        Genera un mapa interactivo con la ubicación dada y lo guarda en un archivo HTML.
        """
        m = folium.Map(location=[lat, lon], zoom_start=12)  # Crea el mapa centrado en la ubicación.
        folium.Marker([lat, lon], popup="Ubicación seleccionada").add_to(m)  # Agrega un marcador con un popup.
        map_path = f'static/maps/map_{map_index}.html'  # Define la ruta donde se guardará el mapa.
        m.save(map_path)  # Guarda el mapa en un archivo HTML.
        return map_path  # Retorna la ruta del archivo.

    @staticmethod
    def get_suggestions(selected_type, selected_weather):
        """
        Genera recomendaciones basadas en el tipo de destino y el clima seleccionado.
        Retorna una lista de sugerencias aleatorias.
        """
        recommendations = []  # Lista que almacenará las recomendaciones.
        df_weather = lecture_weather_recommendations()  # Obtiene las recomendaciones según el clima.
        df_type = lecture_type_recommendations()  # Obtiene las recomendaciones según el tipo.

        if selected_type:  # Si se ha seleccionado un tipo de destino...
            filtered_type = df_type[df_type["Type"] == selected_type]  # Filtra el DataFrame para encontrar coincidencias exactas.
            if not filtered_type.empty:
                recommendations.append(random.choice(filtered_type["Recommendation"].tolist()))  
                # Selecciona una recomendación aleatoria y la agrega a la lista.

        for weather in selected_weather:  # Itera sobre la lista de climas seleccionados.
            filtered_weather = df_weather[df_weather["Weather"] == weather]  # Filtra el DataFrame con el clima actual.
            if not filtered_weather.empty:
                recommendations.append(random.choice(filtered_weather["Recommendation"].tolist()))  
                # Si hay coincidencias, selecciona una recomendación aleatoria y la agrega a la lista.

        return recommendations  # Retorna la lista de recomendaciones obtenidas.