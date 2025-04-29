import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-secreta-muy-segura'
    GOOGLE_CLIENT_ID = os.environ.get('392554787248-rej185egfpq6433f82tc8hq1p9bhabi1.apps.googleusercontent.com')
    GOOGLE_CLIENT_SECRET = os.environ.get('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')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    GOOGLE_REDIRECT_URI = "https://drivelinkv1.onrender.com/login/callback"
