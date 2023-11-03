from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
import psycopg2
from psycopg2 import extras
import json
from flask_session import Session

cliente_bp = Blueprint('cliente', __name__)


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

#Client vista
@cliente_bp.route('/cliente')
@proteger_ruta
def listar_cliente():
    
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        cliente = cursor.fetchall()
        cursor.close()
        return render_template('clientes.html', cliente=cliente)
   

#Agregar cliente 
@cliente_bp.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    
        if request.method == 'POST':
            nombrecliente = request.form['nombre']
            telefonoc = request.form['telefono']
            direccionc = request.form['direccion']
            
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clientes (nombrecliente, telefono, direccion) VALUES (%s, %s, %s)", (nombrecliente, telefonoc, direccionc))
            conn.commit()
            cursor.close()
            flash('Cliente agregado con éxito', 'success')
    
    
        return redirect(url_for('cliente.listar_cliente'))


#----------------------------------------------------------------------------------------------
# Editar empleado
@cliente_bp.route('/editar_cliente/<idcliente>')
def get_cliente(idcliente):
    
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT * FROM clientes WHERE idcliente=%s', (idcliente))
        data = cur.fetchall()
        if data:
            return render_template('edit_cliente.html', cliente=data[0])
        else:
            return jsonify({'mensaje': "Cliente no encontrado"}), 404
    


@cliente_bp.route('/actualizar_cliente/<id>', methods=["POST"])
def update_cliente(id):
    
        if request.method== 'POST':
            nombrecliente=request.form['nombre']
            telefono=request.form['telefono']
            direccion=request.form['direccion']
            cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(""" UPDATE clientes SET nombrecliente=%s, telefono=%s, direccion=%s  WHERE idcliente=%s""", (nombrecliente, telefono, direccion, id))
            conn.commit()
            return redirect(url_for('cliente.listar_cliente'))
   

@cliente_bp.route('/eliminar_cliente/<int:idcliente>')
def eliminar_cliente(idcliente):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE idcliente = %s", (idcliente,))
    conn.commit()
    cursor.close()
    return redirect(url_for('cliente.listar_cliente'))
    
