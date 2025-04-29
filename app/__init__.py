from flask import Flask

def create_app():
       app = Flask(__name__)
       
       # Configuración básica
       app.config.from_object('config.Config')
       
       # Registrar blueprints
       from app.routes import main_bp
       from app.auth import auth_bp
       
       app.register_blueprint(main_bp)
       app.register_blueprint(auth_bp)
       
       return app
