# Importación de los módulos necesarios de Flask y la clase Manipulate
from flask import Flask, render_template, request, jsonify
from services.data import Manipulate

# Creación de la aplicación Flask
app = Flask(__name__)

# Inicialización de la clase Manipulate para manipular los datos
Manipulate()

# Ruta principal de la aplicación (muestra la página inicial)
@app.route('/', methods=['GET'])
def index():
    # Renderiza el archivo index.html que es la página principal de la aplicación
    return render_template('index.html')

# Ruta para realizar la búsqueda con los parámetros enviados desde el formulario
@app.route('/search', methods=['POST'])
def search():
    # Obtiene los datos enviados desde el formulario en la solicitud POST
    selected_type = request.form.get('visitar')  # Tipo de lugar seleccionado
    selected_weather = request.form.getlist('checkbox_group2')  # Clima seleccionado (checkboxes)
    budget = request.form.get('budget')  # Presupuesto ingresado por el usuario
    days = float(request.form.get('days', 0))  # Número de días, por defecto 0 si no se ingresa nada

    # Filtra los datos usando el método 'filters' de la clase Manipulate
    # 'selected_type' y 'selected_weather' son los criterios de filtrado
    filtered_df, locations = Manipulate.filters(selected_type, selected_weather, budget)

    # Obtiene la geolocalización del usuario (latitud y longitud)
    lat, lon = Manipulate.get_geolocation()

    # Lista para almacenar los resultados con las distancias calculadas
    results_with_distances = []
    # Recorre el DataFrame filtrado y calcula la distancia de cada ubicación desde la del usuario
    for row in filtered_df.to_dict(orient='records'):
        # Calcula la distancia entre las coordenadas del usuario y las coordenadas de la ubicación
        distance = Manipulate.calculate_distance(lat, lon, float(row['Lat']), float(row['Long']))
        row['Distance'] = distance  # Añade la distancia al registro de la ubicación
        results_with_distances.append(row)  # Añade el registro con la distancia a la lista de resultados

    # Obtiene las recomendaciones basadas en el tipo de lugar y clima seleccionados
    recommendations = Manipulate.get_suggestions(selected_type, selected_weather)

    # Genera mapas para cada ubicación de los resultados (usando folium o similar)
    for i, row in enumerate(results_with_distances, start=1):
        # Llama a la función para generar un mapa para cada ubicación
        Manipulate.generate_map_for_location(row['Lat'], row['Long'], i)

    # Renderiza el archivo index.html y pasa los resultados y recomendaciones a la plantilla
    return render_template('index.html', results=results_with_distances, days=days, recommendations=recommendations)

# Ejecuta la aplicación Flask en modo de depuración
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)