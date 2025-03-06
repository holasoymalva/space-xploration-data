import requests
import json
import os
from datetime import datetime

# Configuración
JSON_FILE_PATH = "data/space_data.json"
API_URL = "https://api.spacexdata.com/v4/launches/latest"

# Obtener datos de la API
try:
    response = requests.get(API_URL)
    response.raise_for_status()
    space_data = response.json()
except Exception as e:
    print(f"Error al obtener datos: {e}")
    space_data = None

# Asegurar que el directorio existe
os.makedirs(os.path.dirname(JSON_FILE_PATH), exist_ok=True)

# Actualizar archivo JSON
if os.path.exists(JSON_FILE_PATH):
    try:
        with open(JSON_FILE_PATH, "r") as file:
            existing_data = json.load(file)
    except:
        existing_data = {"launches": [], "last_check": ""}
else:
    existing_data = {"launches": [], "last_check": ""}

# Actualizar timestamp
current_time = datetime.now().isoformat()
existing_data["last_check"] = current_time

# Añadir nuevos datos si existen
if space_data:
    existing_ids = [launch.get("id") for launch in existing_data["launches"]]
    if space_data.get("id") not in existing_ids:
        space_data["updated_at"] = current_time
        existing_data["launches"].append(space_data)

# Guardar archivo
with open(JSON_FILE_PATH, "w") as file:
    json.dump(existing_data, file, indent=2)

print("Actualización completada")