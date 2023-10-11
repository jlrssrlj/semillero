from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
import psycopg2
from psycopg2 import extras
from flask_session import Session
import json


app = Flask(__name__)



with open('appsettings.json') as config_file:
    config = json.load(config_file)

db_url = config.get('DefaultConnection')


conn = psycopg2.connect(db_url)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/salir')
def salir():
    return redirect(url_for('index'))
  
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/caja')
def caja():
    return render_template('caja.html')


@app.route('/hacer_login', methods=["POST","GET"])
def hacer_login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        correo = request.form['username']
        password = request.form['password']
        
        cursor.execute('SELECT * FROM empleado WHERE usuario = %s AND clave =%s', (correo, password))
        account = cursor.fetchone()

        if account:
            session['logueado']=True
            return redirect(url_for('listar_productos'))
        else:

            return render_template("login.html")

    return render_template('login.html')

# --------------------------------------------------Producto---------------------------------------------------------------------
#---------------------------------------------------Producto---------------------------------------------------------------------

# Listar productos
@app.route('/productos', methods =['GET'])
def listar_productos():
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        s = "SELECT * FROM producto ORDER BY idproducto ASC"
        cur.execute(s)
        list_users = cur.fetchall()
        return render_template('principalaplicativo.html', list_users=list_users)
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


# Agregar producto
@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    try:
        if request.method == 'POST':
            nombreproducto = request.form['nombreproducto']
            precio = request.form['precio']
            codigo = request.form['codigo']
            idproveedores = request.form['idproveedores']
            
            cursor = conn.cursor()
            cursor.execute("INSERT INTO producto (nombreproducto, precio, codigo, idproveedores) VALUES (%s, %s, %s, %s)", (nombreproducto, precio, codigo,idproveedores))
            conn.commit()
            cursor.close()
        return redirect(url_for('listar_productos'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

# Editar producto
@app.route('/editar_producto/<id>')
def get_producto(id):
    try:
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT*FROM producto WHERE idproducto=%s', (id))
        data=cur.fetchall()
        
        return render_template('edit_producto.html', producto=data[0])
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

@app.route('/actualizar_producto/<id>', methods=["POST"])
def update_producto(id):
    try:
        if request.method== 'POST':
            nombreproducto=request.form['nombreproducto']
            precio=request.form['precio']
            codigo=request.form['codigo']
            idproveedores = request.form['idproveedores']
            cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(""" UPDATE producto SET nombreproducto=%s, precio=%s, codigo=%s, idproveedores=%s  WHERE idproducto=%s""", (nombreproducto,precio,codigo,idproveedores, id))
            conn.commit()
            return redirect(url_for('listar_productos'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

# Eliminar producto
@app.route('/eliminar_producto/<int:idproducto>')
def eliminar_producto(idproducto):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM producto WHERE idproducto = %s", (idproducto,))
        conn.commit()
        cursor.close()
        flash('Producto eliminado con éxito', 'success')
        return redirect(url_for('listar_productos'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


# --------------------------------------------------Proveedores---------------------------------------------------------------------
#---------------------------------------------------Proveedores---------------------------------------------------------------------

@app.route('/proveedores')
def proveedores():
    try:    
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        s="SELECT* FROM proveedores ORDER BY idproveedores ASC"
        cur.execute(s)
        list_users=cur.fetchall()
        return render_template('proveedores.html' ,list_users=list_users  )
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


@app.route('/agregar_proveedor', methods=['POST'])
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
        return redirect(url_for('proveedores'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

# Editar un proveedor
@app.route('/editar_proveedores/<id>')
def get_contact(id):
    try:  
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT*FROM proveedores WHERE idproveedores=%s', (id))
        data=cur.fetchall()
        return render_template('edit_proveedores.html', proveedores=data[0])
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

@app.route('/actualizar/<id>', methods=["POST"])
def update_contact(id):
    try: 
        if request.method== 'POST':
            nombrepro=request.form['nombre']
            nit=request.form['nit']
            direccion=request.form['direccion']
            telefono=request.form['telefono']
            cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(""" UPDATE proveedores SET nombrepro=%s, nit=%s, direccion=%s, telefono=%s  WHERE idproveedores=%s""", (nombrepro,nit,direccion,telefono, id))
            conn.commit()
            return redirect(url_for('proveedores'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

# Eliminar un proveedor
@app.route('/eliminar_proveedores/<string:id>')
def delet_contact(id):
    try:
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('DELETE FROM proveedores WHERE idproveedores={0}'.format(id))
        conn.commit()
        flash('el contacto se a eliminado satisfactoriamente')
        return redirect(url_for('proveedores'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500



#------------------------------------------------------Empleado----------------------------------------------------------------------#

# Listar empleados
@app.route('/empleado')
def listar_empleado():
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        s = "SELECT * FROM empleado ORDER BY idempleado ASC"
        cur.execute(s)
        list_users = cur.fetchall()
        return render_template('empleado.html', list_users=list_users)
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

# Agregar empleado
@app.route('/agregar_empleado', methods=['POST'])
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
        return redirect(url_for('listar_empleado'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

# Editar empleado
@app.route('/editar_empleado/<id>')
def get_empleado(id):
    try:
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT*FROM empleado WHERE idempleado=%s', (id))
        data=cur.fetchall()
        
        return render_template('edit_empleado.html', empleado=data[0])
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

@app.route('/actualizar_empleado/<id>', methods=["POST"])
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
            return redirect(url_for('listar_empleado'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

# Eliminar empleado
@app.route('/eliminar_empleado/<int:idempleado>')
def eliminar_empleado(idempleado):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM empleado WHERE idempleado = %s", (idempleado,))
        conn.commit()
        cursor.close()
        flash('empleado eliminado con éxito', 'success')
        return redirect(url_for('listar_empleado'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

#------------------------------------------------------Clientes----------------------------------------------------------------------#
#------------------------------------------------------Clientes----------------------------------------------------------------------#

#Client vista
@app.route('/cliente')
def listar_cliente():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cliente")
        cliente = cursor.fetchall()
        cursor.close()
        return render_template('clientes.html', cliente=cliente)
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

#Agregar cliente 
@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    try:
        if request.method == 'POST':
            
            nombrecliente = request.form['nombre']
            telefonoc = request.form['telefono']
            direccionc = request.form['direccion']
            
            
            cursor = conn.cursor()
            cursor.execute("INSERT INTO cliente (nombrecliente, telefono, direccion) VALUES (%s,%s,%s)", (nombrecliente,telefonoc,direccionc))
            conn.commit()
            cursor.close()
            flash('cliente agregado con éxito', 'success')
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500
    
    return redirect(url_for('listar_cliente'))

# Editar un Cliente
@app.route('/editar_cliente/<int:idcliente>', methods=['GET', 'POST'])
def editar_cliente(idcliente):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cliente WHERE idcliente = %s", (idcliente))
        cliente = cursor.fetchone()
        
        if request.method == 'POST':
            nombrecliente = request.form['nombre']
            telefonoc = request.form['telefono']
            direccionc = request.form['direccion']
        
            
            cursor = conn.cursor()
            cursor.execute("UPDATE cliente SET nombrecliente=%s, telefono=%s, direccionc=%s WHERE idcliente=%s", (nombrecliente,telefonoc,direccionc,idcliente))
            conn.commit()
            cursor.close()
            flash('cliente actualizado con éxito', 'success')
            return redirect(url_for('listar_cliente'))
        
        return render_template('cliente/editar_cliente.html', cliente=cliente)
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

# Eliminar un cliente
@app.route('/eliminar_cliente/<int:idcliente>')
def eliminar_cliente(idcliente):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cliente WHERE idcliente = %s", (idcliente,))
        conn.commit()
        cursor.close()
        flash('cliente eliminado con éxito', 'success')
        return redirect(url_for('listar_cliente'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


def paginanoencontrada(error):
    return "<h1>La pagina que intenta encontrar no existe<h1>", 404

if __name__ == "__main__":
    app.register_error_handler(404,paginanoencontrada)
    app.run(debug=True, port=5000)
