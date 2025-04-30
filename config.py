import os

class Config:
    # Verificación explícita de variables requeridas
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    if not all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, SECRET_KEY]):
        raise ValueError("Faltan variables de entorno requeridas")
