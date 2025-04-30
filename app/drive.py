from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
from flask import current_app
from flask import session  # Añade esto con las otras importaciones


def get_drive_service():
    if 'google_token' not in session:
        return None
    
    creds = Credentials(
        token=session['google_token'],
        client_id=current_app.config['GOOGLE_CLIENT_ID'],
        client_secret=current_app.config['GOOGLE_CLIENT_SECRET'],
        token_uri='https://oauth2.googleapis.com/token'
    )
    
    return build('drive', 'v3', credentials=creds)

def upload_to_drive(file_path, file_name):
    service = get_drive_service()
    if not service:
        return None
    
    file_metadata = {
        'name': file_name,
        'mimeType': '*/*'
    }
    
    media = MediaFileUpload(file_path, mimetype='*/*', resumable=True)
    
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    
    return file.get('id')
