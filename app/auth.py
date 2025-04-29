from flask import Blueprint, redirect, url_for, session, request
from flask_login import LoginManager, login_user, logout_user, current_user
from oauthlib.oauth2 import WebApplicationClient
import requests
from .models import User

auth_bp = Blueprint('auth', __name__)
login_manager = LoginManager()
client = WebApplicationClient(Config.GOOGLE_CLIENT_ID)

@auth_bp.route("/login")
def login():
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
    
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "Email no verificado por Google.", 400
    
    user = User(
        id_=unique_id, name=users_name, email=users_email
    )
    
    login_user(user)
    session['google_token'] = client.access_token
    
    return redirect(url_for("main.dashboard"))

@auth_bp.route("/logout")
def logout():
    logout_user()
    session.pop('google_token', None)
    return redirect(url_for("main.index"))
