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

#Actualizar arqueo


# Editar arqueo
@arqueo_bp.route('/editar_arqueo/<id>')
def get_contact(id):
    try:  
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT*FROM arqueo WHERE idarqueo=%s', (id))
        data=cur.fetchall()
        return render_template('edit_arqueo.html', arqueo=data[0])
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

@arqueo_bp.route('/actualizarARQ/<id>', methods=["POST"])
def update_contact(id):
    try: 
        if request.method == 'POST':
            monto = request.form['monto'] 
            apertura = request.form['apertura']
            cierra = request.form['cierra']
            idempleado = request.form['idempleado']
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(""" UPDATE arqueo SET monto=%s, apertura=%s, cierra=%s, idempleado=%s  WHERE idarqueo=%s""", (monto, apertura, cierra, idempleado, id))
            conn.commit()
            return redirect(url_for('arqueo.listar_arqueo')) 
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500
    
#Eliminar arqueo

@arqueo_bp.route('/eliminar_arqueo/<int:idarqueo>')
def eliminar_arqueo(idarqueo):
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("DELETE FROM arqueo WHERE idarqueo = %s", (idarqueo,))
        conn.commit()
        flash('El Arqueo se ha eliminado satisfactoriamente')
        return redirect(url_for('listar_arqueo'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500