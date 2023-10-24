from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
import psycopg2
from psycopg2 import extras
import json
from flask_session import Session

empleado_bp = Blueprint('empleado', __name__)


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

@empleado_bp.route('/empleado')
@proteger_ruta
def listar_empleado():
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        mostrar = "SELECT * FROM empleado ORDER BY idempleado ASC"
        cur.execute(mostrar)
        list_users = cur.fetchall()
        return render_template('empleado.html', list_users=list_users)
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

# Agregar empleado
@empleado_bp.route('/agregar_empleado', methods=['POST'])
def agregar_empleado():
    try:
        if request.method == 'POST':
            nombreempleado = request.form['nombreempleado']
            cargo = request.form['cargo']
            correo = request.form['correo']
            usuario = request.form['usuario']
            clave = request.form['clave']
            
            cursor = conn.cursor()
            cursor.execute("INSERT INTO empleado (nombreempleado, cargo, correo, usuario, clave) VALUES (%s, %s, %s, %s, %s)", (nombreempleado, cargo, correo,usuario, clave))
            conn.commit()
            cursor.close()
            return redirect(url_for('empleado.listar_empleado'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

# Editar empleado
@empleado_bp.route('/editar_empleado/<id>')
def get_empleado(id):
    try:
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT*FROM empleado WHERE idempleado=%s', (id))
        data=cur.fetchall()
        
        return render_template('empleado.edit_empleado.html', empleado=data[0])
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

@empleado_bp.route('/actualizar_empleado/<id>', methods=["POST"])
def update_empleado(id):
    try:
        if request.method== 'POST':
            nombreempleado=request.form['nombreempleado']
            cargo=request.form['cargo']
            correo=request.form['correo']
            usuario = request.form['usuario']
            clave = request.form['clave']
            cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(""" UPDATE empleado SET nombreempleado=%s, cargo=%s, correo=%s, usuario=%s, clave=%s  WHERE idempleado=%s""", (nombreempleado, cargo, correo, usuario, clave, id))
            conn.commit()
            return redirect(url_for('empleado.listar_empleado'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

# Eliminar empleado
@empleado_bp.route('/eliminar_empleado/<int:idempleado>')
def eliminar_empleado(idempleado):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM empleado WHERE idempleado = %s", (idempleado,))
        conn.commit()
        cursor.close()
        flash('empleado eliminado con éxito', 'success')
        return redirect(url_for('empleado.listar_empleado'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500