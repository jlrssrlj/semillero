from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import psycopg2
import psycopg2.extras


app = Flask(__name__)

app.secret_key = "prueba"
bcrypt = Bcrypt(app)


#Configuracion base de datos
DB_HOST = "localhost"
DB_NAME = "semillero"
DB_USER = "postgres"
DB_PASS = "1273458"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

def connect_to_database():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/herramienta')
def herramienta():
    return render_template('principalaplicativo.html')

@app.route('/login')
def login():
    return render_template('/login.html')

    
@app.route('/hacer_login', methods=["POST","GET"])
def hacer_login():
    conn = connect_to_database()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        correo = request.form['username']
        password = request.form['password']
        
        cursor.execute('SELECT * FROM empleado WHERE usuario = %s AND clave =%s', (correo, password))
        account = cursor.fetchone()

        if account:
            session['logueado']=True
            return render_template("principalaplicativo.html")
        else:

            return render_template("login.html")

    return render_template('login.html')


cur = conn.cursor()

@app.route('/herramienta')
def index1():
    # Obtén los datos de productos desde la base de datos
    cur.execute("SELECT * FROM producto")
    productos = cur.fetchall()
    return render_template('principalaplicativo.html', productos=productos)

# Ruta para agregar un nuevo producto
@app.route('/add_producto', methods=['POST'])
def add_producto():
    if request.method == 'POST':
        idproducto = request.form['idproducto']
        nombreproducto = request.form['nombreproducto']
        precio = request.form['precio']
        codigo = request.form['codigo']
        idproveedores = request.form['idproveedores']
        # Inserta el nuevo producto en la base de datos
        cur.execute("INSERT INTO producto (idproducto, nombreproducto, precio, codigo, idproveedores) VALUES (%s, %s, %s, %s, %s)", (idproducto, nombreproducto, precio, codigo, idproveedores))
        conn.commit()
    return redirect(url_for('herramienta'))

# Ruta para editar un producto existente
@app.route('/edit_producto/<int:id>', methods=['POST', 'GET'])
def edit_producto(id):
    cur.execute("SELECT * FROM producto WHERE idproducto = %s", (id,))
    producto = cur.fetchone()
    if request.method == 'POST':
        nuevo_idproducto = request.form['idproducto']
        nuevo_nombre = request.form['nombreproducto']
        nuevo_precio = request.form['precio']
        nuevo_codigo = request.form['codigo']
        nuevo_idproveedores = request.form['idproveedores']
        # Actualiza el producto en la base de datos
        cur.execute("UPDATE producto SET idproducto = %s, nombreproducto = %s, precio = %s, codigo = %s, idproveedores = %s WHERE idproducto = %s", (nuevo_idproducto, nuevo_nombre, nuevo_precio, nuevo_codigo, nuevo_idproveedores, id))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', producto=producto)

# Ruta para eliminar un producto
@app.route('/delete_producto/<int:id>')
def delete_producto(id):
    # Elimina el producto de la base de datos
    cur.execute("DELETE FROM producto WHERE idproducto = %s", (id,))
    conn.commit()
    return redirect(url_for('herramienta'))

# --------------------------------------------------------------------------- CLIENTE -----------------------------------------------------------------------------------------------------

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


if __name__ == "__main__":
    app.run(debug=True)
