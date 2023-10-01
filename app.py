from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
from psycopg2 import extras
from flask_session import Session
import json


app = Flask(__name__)
app.secret_key = "prueba"


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
@app.route('/productos')
def listar_productos():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM producto ORDER BY idproducto ASC"
    cur.execute(s)
    list_users = cur.fetchall()
    return render_template('principalaplicativo.html', list_users=list_users)


# Agregar producto
@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
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

# Editar producto
@app.route('/editar_producto/<id>')
def get_producto(id):
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT*FROM producto WHERE idproducto=%s', (id))
    data=cur.fetchall()
    
    return render_template('edit_producto.html', producto=data[0])

@app.route('/actualizar_producto/<id>', methods=["POST"])
def update_producto(id):
    if request.method== 'POST':
        nombreproducto=request.form['nombreproducto']
        precio=request.form['precio']
        codigo=request.form['codigo']
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(""" UPDATE producto SET nombreproducto=%s, precio=%s, codigo=%s WHERE idproducto=%s""", (nombreproducto,precio,codigo, id))
        conn.commit()
        return redirect(url_for('listar_productos'))

# Eliminar producto
@app.route('/eliminar_producto/<int:idproducto>')
def eliminar_producto(idproducto):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM producto WHERE idproducto = %s", (idproducto,))
    conn.commit()
    cursor.close()
    flash('Producto eliminado con éxito', 'success')
    return redirect(url_for('listar_productos'))



# --------------------------------------------------Proveedores---------------------------------------------------------------------
#---------------------------------------------------Proveedores---------------------------------------------------------------------

@app.route('/proveedores')
def proveedores():
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s="SELECT* FROM proveedores ORDER BY idproveedores ASC"
    cur.execute(s)
    list_users=cur.fetchall()
    return render_template('proveedores.html' ,list_users=list_users  )


@app.route('/agregar_proveedor', methods=['POST'])
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
    return redirect(url_for('proveedores'))

# Editar un proveedor
@app.route('/editar_proveedores/<id>')
def get_contact(id):
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT*FROM proveedores WHERE idproveedores=%s', (id))
    data=cur.fetchall()
    return render_template('edit_proveedores.html', proveedores=data[0])

@app.route('/actualizar/<id>', methods=["POST"])
def update_contact(id):
    if request.method== 'POST':
        nombre=request.form['nombre']
        nit=request.form['nit']
        direccion=request.form['direccion']
        telefono=request.form['telefono']
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(""" UPDATE proveedores SET nombre=%s, nit=%s, direccion=%s, telefono=%s  WHERE idproveedores=%s""", (nombre,nit,direccion,telefono, id))
        conn.commit()
        return redirect(url_for('proveedores'))

# Eliminar un proveedor
@app.route('/eliminar_proveedores/<string:id>')
def delet_contact(id):
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('DELETE FROM proveedores WHERE idproveedores={0}'.format(id))
    conn.commit()
    flash('el contacto se a eliminado satisfactoriamente')
    return redirect(url_for('proveedores'))

#------------------------------------------------------Empleado----------------------------------------------------------------------#
#------------------------------------------------------Empleado----------------------------------------------------------------------#

@app.route('/empleado')
def listar_empleado():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleado")
    empleado = cursor.fetchall()
    cursor.close()
    return render_template('empleado.html', empleado=empleado)

@app.route('/agregar_empleado', methods=['POST'])
def agregar_empleado():
    if request.method == 'POST':
        idempleado = request.form['idempleado']
        nombre = request.form['nombre']
        fechaingreso = request.form['fechaingreso']
        fechasalida = request.form['fechasalida']
        cargo = request.form['cargo']
        correo = request.form['correo']
        usuario = request.form['usuario']
        clave = request.form['clave']
        
        cursor = conn.cursor()
        cursor.execute("INSERT INTO empleado (idempleado, nombre, fechaingreso, fechasalida, cargo, correo, usuario, clave) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (idempleado,nombre, fechaingreso, fechasalida, cargo, correo, usuario, clave))
        conn.commit()
        cursor.close()
        flash('Empleado agregado con éxito', 'success')
    
    return redirect(url_for('listar_empleado'))

# Editar un empleado
@app.route('/editar_empleado/<int:idempleado>', methods=['GET', 'POST'])
def editar_empleado(idempleado):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleado WHERE idempleado = %s", (idempleado,))
    empleado = cursor.fetchone()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        fechaingreso = request.form['fechaingreso']
        fechasalida = request.form['fechasalida']
        cargo = request.form['cargo']
        correo = request.form['correo']
        usuario = request.form['usuario']
        clave = request.form['clave']
        
        cursor = conn.cursor()
        cursor.execute("UPDATE empleado SET nombre = %s, fechaingreso = %s, fechasalida = %s, cargo = %s, correo = %s, usuario = %s, clave = %s", (nombre, fechaingreso, fechasalida, cargo, correo, usuario, clave))
        conn.commit()
        cursor.close()
        flash('Empleado actualizado con éxito', 'success')
        return redirect(url_for('listar_empleado'))
    
    return render_template('empleado/editar_empleado.html', empleado=empleado)

# Eliminar un empleado
@app.route('/eliminar_empleado/<int:idempleado>')
def eliminar_empleado(idempleado):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleado WHERE idempleado = %s", (idempleado,))
    conn.commit()
    cursor.close()
    flash('Empleado eliminado con éxito', 'success')
    return redirect(url_for('listar_empleado'))

#------------------------------------------------------Clientes----------------------------------------------------------------------#
#------------------------------------------------------Clientes----------------------------------------------------------------------#

#Client vista
@app.route('/cliente')
def listar_cliente():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cliente")
    cliente = cursor.fetchall()
    cursor.close()
    return render_template('clientes.html', cliente=cliente)

#Agregar cliente 
@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    if request.method == 'POST':
        idcliente = request.form['idcliente']
        nombrec = request.form['nombre']
        telefonoc = request.form['telefono']
        direccionc = request.form['direccion']
        
        
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cliente (idcliente, nombrec, telefonoc, direccionc) VALUES (%s,%s,%s,%s)", (idcliente,nombrec,telefonoc,direccionc))
        conn.commit()
        cursor.close()
        flash('cliente agregado con éxito', 'success')
    
    return redirect(url_for('listar_cliente'))

# Editar un Cliente
@app.route('/editar_cliente/<int:idcliente>', methods=['GET', 'POST'])
def editar_cliente(idcliente):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cliente WHERE idcliente = %s", (idcliente))
    cliente = cursor.fetchone()
    
    if request.method == 'POST':
        nombrec = request.form['nombre']
        telefonoc = request.form['telefono']
        direccionc = request.form['direccion']
       
        
        cursor = conn.cursor()
        cursor.execute("UPDATE cliente SET nombrec=%s, telefonoc=%s, direccionc=%s WHERE idcliente=%s", (nombrec,telefonoc,direccionc,idcliente))
        conn.commit()
        cursor.close()
        flash('cliente actualizado con éxito', 'success')
        return redirect(url_for('listar_cliente'))
    
    return render_template('cliente/editar_cliente.html', cliente=cliente)

# Eliminar un cliente
@app.route('/eliminar_cliente/<int:idcliente>')
def eliminar_cliente(idcliente):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cliente WHERE idcliente = %s", (idcliente,))
    conn.commit()
    cursor.close()
    flash('cliente eliminado con éxito', 'success')
    return redirect(url_for('listar_cliente'))



if __name__ == "__main__":
    app.run(debug=True)
