from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from conection import get_db_connection
from datetime import datetime

caja_bp = Blueprint('caja', __name__)

def proteger_ruta(func):
    def wrapper(*args, **kwargs):
        if 'logueado' in session and session['logueado']:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    wrapper.__name__ = func.__name__
    return wrapper

carrito = []

def obtener_productos():
    try:
        with get_db_connection() as mydb:
            cur = mydb.cursor()
            cur.execute("SELECT idproducto, nombreproducto, precio, codigo FROM productos")
            productos = cur.fetchall()
        return productos
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


@caja_bp.route('/caja', methods=['GET'])
@proteger_ruta
def caja():
    productos = obtener_productos()  
    return render_template('caja.html', productos=productos, carrito=carrito)

@caja_bp.route('/agregar', methods=['POST'])
@proteger_ruta
def agregar():
    try:
        with get_db_connection() as mydb:
            idproducto = request.form.get('idproducto')
            cur = mydb.cursor()
            cur.execute("SELECT nombreproducto, precio, codigo FROM productos WHERE idproducto = %s", (idproducto,))
            producto = cur.fetchone()

            if producto:
                # Obtén la cantidad del formulario
                cantidad = int(request.form.get('cantidad'))

                # Agrega el producto al carrito como un diccionario
                producto_dict = {
                    'nombreproducto': producto[0],
                    'precio': producto[1],
                    'codigo': producto[2],
                    'cantidad': cantidad,
                }
                carrito.append(producto_dict)
                
            # Actualiza la lista de productos
            productos = obtener_productos()

            return render_template('caja.html', productos=productos, carrito=carrito)
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

@caja_bp.route('/obtener_clientes')
@proteger_ruta
def obtener_clientes():
    try:
        with get_db_connection() as mydb:
            cur = mydb.cursor()
            cur.execute("SELECT idcliente, nombrecliente FROM clientes")
            clientes = cur.fetchall()
            
            # Formatear la respuesta como una lista de diccionarios
            clientes_data = [{'idcliente': cliente[0], 'nombrecliente': cliente[1]} for cliente in clientes]
            
            return jsonify(clientes_data)  # Devolver la lista formateada como JSON
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500