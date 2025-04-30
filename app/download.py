import os
import requests
from urllib.parse import urlparse
from flask import current_app

def download_file(url, download_folder):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Lanza error para respuestas 4XX/5XX
        
        filename = os.path.basename(urlparse(url).path) or 'downloaded_file'
        file_path = os.path.join(download_folder, filename)
        
        os.makedirs(download_folder, exist_ok=True)
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filtra keep-alive chunks
                    f.write(chunk)
        
        return file_path, filename
    
    except Exception as e:
        current_app.logger.error(f"Error al descargar {url}: {str(e)}")
        return None, None
