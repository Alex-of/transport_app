# transport_app/routes.py

from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from .models import db, User, KPIFile
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_bcrypt import Bcrypt
import os

bcrypt = Bcrypt()

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Hello, World!"  # Ruta de prueba

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        kpi_type = request.form['kpi_type']
        if file and kpi_type:
            filename = secure_filename(file.filename)
            file.save(os.path.join('uploads', filename))
            new_file = KPIFile(filename=filename, date_uploaded=datetime.utcnow(), kpi_type=kpi_type)
            db.session.add(new_file)
            db.session.commit()
            flash('File successfully uploaded', 'success')
            return redirect(url_for('main.kpis'))
    return render_template('upload.html')

@main.route('/kpis')
@login_required
def kpis():
    kpi_files = KPIFile.query.all()
    return render_template('kpis.html', kpi_files=kpi_files)
