from flask import Blueprint, render_template, request, redirect, url_for, flash
import psycopg2
import json

proveedores_bp = Blueprint('proveedores', __name__)

with open('appsettings.json') as config_file:
    config = json.load(config_file)

db_url = config.get('DefaultConnection')


conn = psycopg2.connect(db_url)

@proveedores_bp.route('/proveedores')
def listar_proveedores():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM proveedores")
    proveedores = cursor.fetchall()
    cursor.close()
    return render_template('proveedores/listar_proveedores.html', proveedores=proveedores)

# Agregar un nuevo proveedor
@proveedores_bp.route('/agregar_proveedor', methods=['POST'])
def agregar_proveedor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        nit = request.form['nit']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        
        cursor = conn.cursor()
        cursor.execute("INSERT INTO proveedores (nombre, nit, direccion, telefono) VALUES (%s, %s, %s, %s)", (nombre, nit, direccion, telefono))
        conn.commit()
        cursor.close()
        flash('Proveedor agregado con éxito', 'success')
    
    return redirect(url_for('proveedores.listar_proveedores'))

# Editar un proveedor
@proveedores_bp.route('/editar_proveedor/<int:idproveedores>', methods=['GET', 'POST'])
def editar_proveedor(idproveedores):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM proveedores WHERE idproveedores = %s", (idproveedores,))
    proveedor = cursor.fetchone()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        nit = request.form['nit']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        
        cursor = conn.cursor()
        cursor.execute("UPDATE proveedores SET nombre=%s, nit=%s, direccion=%s, telefono=%s WHERE idproveedores=%s", (nombre, nit, direccion, telefono, idproveedores))
        conn.commit()
        cursor.close()
        flash('Proveedor actualizado con éxito', 'success')
        return redirect(url_for('proveedores.listar_proveedores'))
    
    return render_template('proveedores/editar_proveedor.html', proveedor=proveedor)

# Eliminar un proveedor
@proveedores_bp.route('/eliminar_proveedor/<int:idproveedores>')
def eliminar_proveedor(idproveedores):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM proveedores WHERE idproveedores = %s", (idproveedores,))
    conn.commit()
    cursor.close()
    flash('Proveedor eliminado con éxito', 'success')
    return redirect(url_for('proveedores.listar_proveedores'))
