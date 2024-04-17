import requests
import folium
import psycopg2
import math

# Parámetros de conexión a la base de datos
conn_params = {
    "host": "localhost",
    "database": "postgis",
    "user": "chortax",
    "password": "123"
}

# Intenta establecer la conexión a la base de datos
try:
    conn = psycopg2.connect(**conn_params)
    print("Conexión exitosa a la base de datos")
except psycopg2.Error as e:
    print("Error al conectar a la base de datos:", e)

# Si la conexión fue exitosa, continúa con el resto del código
if conn:
    # Crea un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # Consulta para obtener las coordenadas de los enlaces
    query = """
    SELECT source.lat AS source_lat, source.lon AS source_lon, 
           target.lat AS target_lat, target.lon AS target_lon
    FROM links
    JOIN nodes AS source ON links.source = source.id_node
    JOIN nodes AS target ON links.target = target.id_node
    """

    # Ejecuta la consulta
    cursor.execute(query)

    # Almacena las coordenadas de los enlaces
    coordenadas_links = cursor.fetchall()

    # Cierra el cursor
    cursor.close()

    # Cierra la conexión a la base de datos
    conn.close()

    # URL del feed de terremotos
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"

    # Obtiene los datos de terremotos
    respuesta = requests.get(url)
    terremotos = respuesta.json()

    # Crea el mapa de Folium
    mapa = folium.Map(location=[0, 0], zoom_start=2)

    # Función para calcular el radio afectado por el terremoto usando la ley de Omori
    def calcular_radio_afectado(magnitud):
        return 10 ** (0.5 * magnitud + 1.05)

    # Itera sobre los terremotos
    for terremoto in terremotos["features"]:
        lugar = terremoto["properties"]["place"]
        if "Italy" in lugar:
            coordenadas = terremoto["geometry"]["coordinates"]
            magnitud = terremoto["properties"]["mag"]
            
            # Calcula el radio afectado por el terremoto
            radio_afectado = calcular_radio_afectado(magnitud)

            # Agrega un círculo rojo al mapa representando el área afectada
            folium.Circle(
                location=[coordenadas[1], coordenadas[0]],
                radius=radio_afectado * 1000,  # Convierte de kilómetros a metros
                color='red',
                fill=True,
                fill_color='red',
                fill_opacity=0.3,
            ).add_to(mapa)

            # Agrega un marcador al mapa para el terremoto
            folium.Marker(
                location=[coordenadas[1], coordenadas[0]],
                popup=f"{lugar}, Magnitud: {magnitud}",
                icon=folium.Icon(color="red")
            ).add_to(mapa)

    # Itera sobre los enlaces y dibuja líneas azules en el mapa
    for source_lat, source_lon, target_lat, target_lon in coordenadas_links:
        folium.PolyLine([(source_lat, source_lon), (target_lat, target_lon)], color="blue").add_to(mapa)

    # Guarda el mapa como un archivo HTML
    mapa.save("terremotos.html")
