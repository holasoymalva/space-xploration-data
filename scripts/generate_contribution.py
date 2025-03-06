import json
import os
import random
import datetime

# Crear directorio si no existe
os.makedirs('contributions', exist_ok=True)

# Generar timestamp único
now = datetime.datetime.utcnow()
timestamp = now.strftime('%Y-%m-%dT%H:%M:%SZ')
date_time = now.strftime('%Y-%m-%d_%H-%M-%S')
random_num = random.randint(1, 1000)

# Crear archivo de contribución con timestamp
contribution_data = {
    "timestamp": timestamp,
    "random_value": random_num,
    "message": "Actualización automática de datos"
}

with open(f"contributions/update_{date_time}.json", 'w') as f:
    json.dump(contribution_data, f, indent=2)

# Actualizar archivo summary o crearlo si no existe
summary_path = 'contributions/summary.json'
if os.path.exists(summary_path):
    try:
        with open(summary_path, 'r') as f:
            summary = json.load(f)
    except:
        summary = {'updates': [], 'total_updates': 0}
else:
    summary = {'updates': [], 'total_updates': 0}

# Añadir nueva actualización
new_update = {
    'timestamp': timestamp,
    'file': f'update_{date_time}.json'
}
summary['updates'].append(new_update)
summary['total_updates'] = len(summary['updates'])
summary['last_update'] = timestamp

# Guardar archivo summary
with open(summary_path, 'w') as f:
    json.dump(summary, f, indent=2)

print(f"Contribución generada: update_{date_time}.json")