from flask import Blueprint, redirect, url_for, session, request
from flask_login import LoginManager, login_user, logout_user, current_user
from oauthlib.oauth2 import WebApplicationClient
import requests
from .models import User
from app.models import User
from config import Config
from flask_login import login_required
from app import login_manager


auth_bp = Blueprint('auth', __name__)
#login_manager = LoginManager()
client = WebApplicationClient(Config.GOOGLE_CLIENT_ID)

from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@auth_bp.route("/login")
def login():
    # --- DEBUG: Verificar credenciales (eliminar después) ---
    print("CLIENT_ID:", Config.GOOGLE_CLIENT_ID)
    print("CLIENT_SECRET:", bool(Config.GOOGLE_CLIENT_SECRET))
    # -------------------------------------------------------
    
    google_provider_cfg = requests.get(Config.GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile", "https://www.googleapis.com/auth/drive.file"],
    )
    return redirect(request_uri)


@auth_bp.route("/login/callback")
def callback():
    code = request.args.get("code")
    
    google_provider_cfg = requests.get(Config.GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]
    
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(Config.GOOGLE_CLIENT_ID, Config.GOOGLE_CLIENT_SECRET),
    )
    
    client.parse_request_body_response(token_response.text)
    
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.status_code != 200:
            raise ValueError(f"Error obteniendo userinfo: {userinfo_response.text}")
    user_data = userinfo_response.json()
        
    if not user_data.get("email_verified"):
            return "Email no verificado por Google", 400
            
    user = User(
            id_=user_data["sub"],
            name=user_data.get("given_name", ""),
            email=user_data["email"]
        )
        
    login_user(user)
    session['google_token'] = client.access_token
        
    return redirect(url_for("main.dashboard"))
    
  except Exception as e:
        print(f"Error en callback: {str(e)}")  # Ver en logs de Render
        return "Error en autenticación", 500




@auth_bp.route("/logout")
def logout():
    logout_user()
    session.pop('google_token', None)
    return redirect(url_for("main.index"))

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

