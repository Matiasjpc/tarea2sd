from elasticsearch import Elasticsearch

# Configuración de conexión con Elasticsearch
es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "matias".encode('utf-8')),  # Cambia "tu_contraseña" por tu contraseña real y asegúrate de usar utf-8
)

# Prueba de conexión y creación de índice
try:
    # Crear índice si no existe
    if not es.indices.exists(index="orders"):
        es.indices.create(index="orders")
        print("Índice 'orders' creado en Elasticsearch")
    else:
        print("Índice 'orders' ya existe en Elasticsearch")
except Exception as e:
    print(f"Error de conexión: {e}")
