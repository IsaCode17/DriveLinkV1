import os

class Config:
    # Credenciales de Google
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"  # <-- Añade esta línea
    
    # Configuración general
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    
    # Validación
    if not all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET]):
        raise ValueError("Faltan credenciales de Google OAuth")
