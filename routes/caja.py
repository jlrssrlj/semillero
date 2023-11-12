from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from conection import get_db_connection
from datetime import datetime, date

caja_bp = Blueprint('caja', __name__)
mydb = get_db_connection()
def proteger_ruta(func):
    def wrapper(*args, **kwargs):
        if 'logueado' in session and session['logueado']:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    wrapper.__name__ = func.__name__
    return wrapper

def verificar_arqueo():
    today = date.today()
    cur = mydb.cursor()
    cur.execute("SELECT * FROM arqueos WHERE apertura = %s", (today,))
    result = cur.fetchone()
    cur.close()
    
    return result

@caja_bp.route('/caja', methods=['GET'])
@proteger_ruta
def caja():
    arqueo_existente = verificar_arqueo()
    if arqueo_existente is not None:
        arqueo_existente_hoy = arqueo_existente[2] == date.today()
        print(arqueo_existente_hoy)  # Verifica si es True o False
    else:
        arqueo_existente_hoy = False  # O establece un valor por defecto
    
    cur = mydb.cursor()
    cur.execute("SELECT * FROM productos")
    productos = cur.fetchall()
    cur.close()
    
    return render_template('caja.html', productos=productos, arqueo_existente=arqueo_existente_hoy)
    
@caja_bp.route('/agregar', methods=['POST'])
@proteger_ruta
def agregar():
    if request.method == 'POST':
        id_producto = request.form['idproducto']
        nombre = request.form['nombre']
        fecha_hora = datetime.now()
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        id_empleado = session.get('idempleado') 
        nombre_empleado = session.get('nombre_empleado')
        
        cur = mydb.cursor()
        cur.execute("INSERT INTO carrito (id_empleado, id_producto, nombre, fecha_hora, valor, cantidad) VALUES (%s, %s, %s, %s, %s, %s)",
                    (id_empleado, id_producto, nombre, fecha_hora, precio, cantidad))
        mydb.commit()
        cur.close()