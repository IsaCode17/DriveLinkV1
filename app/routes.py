from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from .auth import login_required
from .download import download_file
from .drive import upload_to_drive
from flask_login import login_required
import os
import tempfile
import shutil
from flask import session, flash, redirect, url_for, request


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@main_bp.route('/transfer', methods=['POST'])
@login_required
def transfer():
    download_url = request.form.get('download_url')
    if not download_url:
        flash('Por favor ingresa una URL válida', 'error')
        return redirect(url_for('main.dashboard'))
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Descargar archivo
        file_path, filename = download_file(download_url, temp_dir)
        if not file_path:
            flash('Error al descargar el archivo', 'error')
            return redirect(url_for('main.dashboard'))
        
        # Subir a Google Drive
        file_id = upload_to_drive(file_path, filename)
        if file_id:
            flash(f'Archivo {filename} subido correctamente a Google Drive!', 'success')
        else:
            flash('Error al subir el archivo a Google Drive', 'error')
        
    except Exception as e:
        flash(f'Error en el proceso: {str(e)}', 'error')
        return redirect(url_for('main.dashboard'))
    
    finally:
        # Limpieza segura del directorio temporal
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)  # Elimina recursivamente
            except Exception as e:
                print(f"Error limpiando directorio temporal: {e}")
    
    return redirect(url_for('main.dashboard'))
