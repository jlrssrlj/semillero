from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
import psycopg2
from psycopg2 import extras
import json
from flask_session import Session

productos_bp = Blueprint('productos', __name__)


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

@productos_bp.route('/productos', methods =['GET'])
@proteger_ruta
def listar_productos():
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        s = "SELECT * FROM productos ORDER BY idproducto ASC"
        cur.execute(s)
        list_users = cur.fetchall()
        return render_template('principalaplicativo.html', list_users=list_users)
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


# Agregar producto
@productos_bp.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    try:
        if request.method == 'POST':
            nombreproducto = request.form['nombreproducto']
            precio = request.form['precio']
            codigo = request.form['codigo']
            idproveedores = request.form['idproveedores']            
            stock = request.form['stock']
            cursor = conn.cursor()
            cursor.execute("INSERT INTO productos (nombreproducto, precio, codigo, idproveedores, cantidad) VALUES (%s, %s, %s, %s, %s)", (nombreproducto, precio, codigo,idproveedores,stock))
            conn.commit()
            cursor.close()
        return redirect(url_for('productos.listar_productos'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


# Editar producto
@productos_bp.route('/editar_producto/<id>')
def get_producto(id):
    try:
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT*FROM productos WHERE idproducto=%s', (id))
        data=cur.fetchall()
        
        return render_template('edit_producto.html', producto=data[0])
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

@productos_bp.route('/actualizar_producto/<id>', methods=["POST"])
def update_producto(id):
    try:
        if request.method== 'POST':
            nombreproducto=request.form['nombreproducto']
            precio=request.form['precio']
            codigo=request.form['codigo']
            idproveedores = request.form['idproveedores']
            stock = request.form['stock']
            cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(""" UPDATE productos SET nombreproducto=%s, precio=%s, codigo=%s, idproveedores=%s, cantidad=%s  WHERE idproducto=%s""", (nombreproducto,precio,codigo,idproveedores,stock, id))
            conn.commit()
            return redirect(url_for('productos.listar_productos'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


# Eliminar producto
@productos_bp.route('/eliminar_producto/<int:idproducto>')
def eliminar_producto(idproducto):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ventas WHERE idproducto = %s", (idproducto,))
        cursor.execute("DELETE FROM productos WHERE idproducto = %s", (idproducto,))
        conn.commit()
        cursor.close()
        flash('Producto eliminado con éxito', 'success')
        return redirect(url_for('productos.listar_productos'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500




