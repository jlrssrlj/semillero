from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
import psycopg2
from psycopg2 import extras
import json
from flask_session import Session

arqueo_bp = Blueprint('arqueo', __name__)


with open('appsettings.json') as config_file:
    config = json.load(config_file)

db_url = config.get('DefaultConnection')


conn = psycopg2.connect(db_url)

def proteger_ruta(func):
    def wrapper(*args, **kwargs):
        if 'logueado' in session and session['logueado']:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    wrapper.__name__ = func.__name__
    return wrapper

#Mostrar la tabla de arqueo
@arqueo_bp.route('/arqueo')
def listar_arqueo():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM arqueo"
    cur.execute(s)
    list_users = cur.fetchall()
    return render_template('arqueo.html',  list_users= list_users)

# Agregar Caja
@arqueo_bp.route('/agregar_arqueo', methods=['POST'])
def agregar_arqueo():
    if request.method == 'POST':
        monto = request.form['monto'] 
        apertura = request.form['apertura']
        cierra = request.form['cierra']
        idempleado = request.form['idempleado']
        
        cursor = conn.cursor()
        cursor.execute("INSERT INTO arqueo (monto, apertura, cierra, idempleado) VALUES (%s, %s, %s, %s)", (monto, apertura, cierra, idempleado))
        conn.commit()
        cursor.close()
    return redirect(url_for('listar_arqueo'))