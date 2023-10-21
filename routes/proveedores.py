from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
import psycopg2
from psycopg2 import extras
import json
from flask_session import Session

proveedores_bp = Blueprint('proveedores', __name__)


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

@proveedores_bp.route('/proveedores')
@proteger_ruta
def proveedores():
    try:    
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        s="SELECT* FROM proveedores ORDER BY idproveedores ASC"
        cur.execute(s)
        list_users=cur.fetchall()
        return render_template('proveedores.html' ,list_users=list_users  )
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


@proveedores_bp.route('/agregar_proveedor', methods=['POST'])
def agregar_proveedor():
    try:  
        if request.method == 'POST':
            nombrepro = request.form['nombre']
            nit = request.form['nit']
            direccion = request.form['direccion']
            telefono = request.form['telefono']
            
            cursor = conn.cursor()
            cursor.execute("INSERT INTO proveedores (nombrepro, nit, direccion, telefono) VALUES (%s, %s, %s, %s)", (nombrepro, nit, direccion, telefono))
            conn.commit()
            cursor.close()
        return redirect(url_for('proveedores.proveedores'))  # Cambia 'proveedores.listar_proveedores' a 'proveedores.proveedores'
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


# Editar un proveedor
@proveedores_bp.route('/editar_proveedores/<id>')
def get_contact(id):
    try:  
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT*FROM proveedores WHERE idproveedores=%s', (id))
        data=cur.fetchall()
        return render_template('edit_proveedores.html', proveedores=data[0])
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

@proveedores_bp.route('/actualizar/<id>', methods=["POST"])
def update_contact(id):
    try: 
        if request.method == 'POST':
            nombrepro = request.form['nombre']
            nit = request.form['nit']
            direccion = request.form['direccion']
            telefono = request.form['telefono']
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""UPDATE proveedores SET nombrepro=%s, nit=%s, direccion=%s, telefono=%s  WHERE idproveedores=%s""", (nombrepro, nit, direccion, telefono, id))
            conn.commit()
            return redirect(url_for('proveedores.proveedores'))  # Cambia 'proveedores' a 'proveedores.proveedores'
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


# Eliminar un proveedor
@proveedores_bp.route('/eliminar_proveedores/<string:id>')
def delete_contact(id):
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('DELETE FROM proveedores WHERE idproveedores = %s', (id,))
        conn.commit()
        flash('El contacto se ha eliminado satisfactoriamente')
        return redirect(url_for('proveedores.proveedores'))  # Cambia 'proveedores' a 'proveedores.proveedores'
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500