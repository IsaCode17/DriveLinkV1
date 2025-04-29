import requests
import os
from urllib.parse import urlparse
from flask import current_app

def download_file(url, download_folder):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Obtener nombre del archivo de la URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path) or 'downloaded_file'
        
        # Crear carpeta de descargas si no existe
        os.makedirs(download_folder, exist_ok=True)
        
        # Guardar archivo
        file_path = os.path.join(download_folder, filename)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        return file_path, filename
    
    except Exception as e:
        current_app.logger.error(f"Error al descargar archivo: {e}")
        return None, None
