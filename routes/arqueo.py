from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from conection import get_db_connection
import datetime
from flask_session import Session

# Crear el blueprint
arqueo_bp = Blueprint('arqueo', __name__)

# Obtener la conexión de la base de datos y el cursor
mydb = get_db_connection()

# Definir el decorador para proteger la ruta
def proteger_ruta(func):
    def wrapper(*args, **kwargs):
        if 'logueado' in session and session['logueado']:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    wrapper.__name__ = func.__name__
    return wrapper

# Mostrar la tabla de arqueo
@arqueo_bp.route('/arqueo')
def listar_arqueo():
    cur = mydb.cursor()
    s = "SELECT * FROM arqueos"
    cur.execute(s)
    list_users = cur.fetchall()
    cur.close()
    return render_template('arqueo.html', list_users=list_users)

# Agregar Caja
@arqueo_bp.route('/agregar_arqueo', methods=['POST'])
def agregar_arqueo():
    if request.method == 'POST':
        cur = mydb.cursor()
        monto = request.form['monto']
        # Capturar la fecha y hora actual al momento de la apertura
        apertura = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cierra = None  # Establecer como None inicialmente, ya que se registrará al momento del cierre
        idempleado = request.form['idempleado']
 
        cur.execute("INSERT INTO arqueos (monto, apertura, cierre, idempleado) VALUES (%s, %s, %s, %s)", (monto, apertura, cierra, idempleado))
        mydb.commit()
        cur.close()
    return redirect(url_for('arqueo.listar_arqueo'))
@arqueo_bp.route('/actualizar_arqueo/<int:idarqueo>', methods=['POST'])
def actualizar_arqueo(idarqueo):
    if request.method == 'POST':
        cur = mydb.cursor()
        monto = request.form['monto']
        # Capturar la fecha y hora actual al momento del cierre
        cierra = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        idempleado = request.form['idempleado']

        cur.execute("UPDATE arqueos SET monto=%s, cierra=%s, idempleado=%s WHERE idarqueo=%s", (monto, cierra, idempleado, idarqueo))
        mydb.commit()
        cur.close()
    return redirect(url_for('arqueo.listar_arqueo'))

#Eliminar arqueo
@arqueo_bp.route('/eliminar_arqueo/<int:idarqueo>')
def eliminar_arqueo(idarqueo):
    try:
        cur = mydb.cursor()
        cur.execute("DELETE FROM arqueos WHERE idarqueo = %s", (idarqueo,))
        mydb.commit()
        cur.close()
        return redirect(url_for('arqueo.listar_arqueo'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500
