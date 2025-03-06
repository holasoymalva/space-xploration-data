#!/usr/bin/env python3
import requests
import json
import os
import time
import git
from datetime import datetime

# Configuración
REPO_URL = "https://github.com/holasoymalva/space-xploration-data.git"
LOCAL_REPO_PATH = "space-xploration-data"
JSON_FILE_PATH = "data/space_data.json"
API_URL = "https://api.spacexdata.com/v4/launches/latest"  # API de SpaceX como ejemplo
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # Token de GitHub almacenado como variable de entorno
UPDATE_INTERVAL = 60  # Intervalo de actualización en segundos (1 minuto)

def fetch_space_data():
    """Obtener datos de la API espacial"""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de la API: {e}")
        return None

def update_json_file(repo_path, file_path, new_data):
    """Actualizar el archivo JSON con los nuevos datos y timestamp"""
    full_path = os.path.join(repo_path, file_path)
    
    # Crear directorios si no existen
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # Timestamp actual
    current_time = datetime.now().isoformat()
    
    # Leer datos existentes si el archivo existe
    if os.path.exists(full_path):
        try:
            with open(full_path, 'r') as file:
                existing_data = json.load(file)
        except json.JSONDecodeError:
            existing_data = {"launches": [], "last_check": ""}
    else:
        existing_data = {"launches": [], "last_check": ""}
    
    # Actualizar siempre el timestamp de última verificación
    existing_data["last_check"] = current_time
    
    # Agregar nuevos datos si están disponibles y no existen ya
    if new_data:
        existing_ids = [launch.get("id") for launch in existing_data["launches"]]
        if new_data.get("id") not in existing_ids:
            # Añadir timestamp de actualización
            new_data["updated_at"] = current_time
            existing_data["launches"].append(new_data)
    
    # Guardar archivo JSON actualizado (siempre, para actualizar al menos el timestamp)
    with open(full_path, 'w') as file:
        json.dump(existing_data, file, indent=2)
    
    # Siempre retornamos True para forzar el commit
    return True

def setup_repository():
    """Configurar el repositorio local"""
    if os.path.exists(LOCAL_REPO_PATH):
        # Si el repositorio ya existe, actualizarlo
        repo = git.Repo(LOCAL_REPO_PATH)
        origin = repo.remotes.origin
        origin.pull()
    else:
        # Clonar el repositorio si no existe
        repo = git.Repo.clone_from(REPO_URL, LOCAL_REPO_PATH)
        
    # Configurar credenciales si se proporciona un token
    if GITHUB_TOKEN:
        with repo.config_writer() as git_config:
            git_config.set_value('user', 'name', 'Space Data Bot')
            git_config.set_value('user', 'email', 'bot@example.com')
        
        # Actualizar URL remota para incluir el token
        if GITHUB_TOKEN:
            token_url = f"https://{GITHUB_TOKEN}@github.com/holasoymalva/space-xploration-data.git"
            repo.remotes.origin.set_url(token_url)
    
    return repo

def commit_and_push_changes(repo, file_path):
    """Realizar commit y push de los cambios, forzando commit incluso sin cambios"""
    try:
        repo.git.add(file_path)
        
        # Realizar commit siempre, incluso si no hay cambios
        commit_message = f"Actualización automática de datos espaciales - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        try:
            # Intentar commit normal primero
            repo.git.commit('-m', commit_message)
        except git.GitCommandError as e:
            # Si falla porque no hay cambios, forzar commit vacío
            if "nothing to commit" in str(e):
                repo.git.commit('-m', commit_message, '--allow-empty')
            else:
                # Si es otro error, propagarlo
                raise
        
        # Push a GitHub
        repo.remotes.origin.push()
        print(f"Cambios enviados a GitHub: {commit_message}")
        return True
    except git.GitCommandError as e:
        print(f"Error de Git: {e}")
        return False

def main():
    print("Iniciando script de actualización de datos espaciales...")
    
    # Configurar el repositorio
    repo = setup_repository()
    
    while True:
        print(f"Obteniendo datos espaciales a las {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Obtener datos espaciales
        space_data = fetch_space_data()
        
        # Actualizar archivo JSON (siempre retorna True)
        updated = update_json_file(LOCAL_REPO_PATH, JSON_FILE_PATH, space_data)
        
        # Commit y push de los cambios (siempre)
        commit_and_push_changes(repo, JSON_FILE_PATH)
        
        print(f"Esperando {UPDATE_INTERVAL} segundos hasta la próxima actualización...")
        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    main()