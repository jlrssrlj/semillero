from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import json


app = Flask(__name__)
app.secret_key = "prueba"



# Cargar la configuración desde appsettings.json
with open('appsettings.json') as config_file:
    config = json.load(config_file)

db_url = config.get('DefaultConnection')

# Configurar la conexión a la base de datos PostgreSQL
conn = psycopg2.connect(db_url)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def prodcutos():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()
    cursor.close()
    return render_template('principalaplicativo.html', productos=productos)

@app.route('/herramienta')
def herramienta():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()
    cursor.close()
    return render_template('principalaplicativo.html', productos=productos)

@app.route('/login')
def login():
    return render_template('login.html')

# Listar productos
@app.route('/productos')
def listar_productos():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()
    cursor.close()
    return render_template('principalaplicativo.html', productos=productos)

# Agregar producto
@app.route('/agregar', methods=['POST'])
def agregar_producto():
    if request.method == 'POST':
        idproducto = request.form['idproducto']
        nombreproducto = request.form['nombreproducto']
        precio = request.form['precio']
        codigo = request.form['codigo']
        idproveedores = request.form['idproveedores']
        
        cursor = conn.cursor()
        cursor.execute("INSERT INTO producto (idproducto, nombreproducto, precio, codigo, idproveedores) VALUES (%s, %s, %s, %s, %s)", (idproducto, nombreproducto, precio, codigo, idproveedores))
        conn.commit()
        cursor.close()
        flash('Producto agregado con éxito', 'success')
    
    return redirect(url_for('listar_productos'))

# Editar producto
@app.route('/editar_producto/<int:idproducto>', methods=['GET', 'POST'])
def editar_producto(idproducto):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto WHERE idproducto = %s", (idproducto,))
    producto = cursor.fetchone()
    
    if request.method == 'POST':
        nombreproducto = request.form['nombreproducto']
        precio = request.form['precio']
        codigo = request.form['codigo']
        idproveedores = request.form['idproveedores']
        
        cursor = conn.cursor()
        cursor.execute("UPDATE producto SET nombreproducto=%s, precio=%s, codigo=%s, idproveedores=%s WHERE idproducto=%s", (nombreproducto, precio, codigo, idproveedores, idproducto))
        conn.commit()
        cursor.close()
        flash('Producto actualizado con éxito', 'success')
        return redirect(url_for('listar_productos'))
    
    return render_template('principalaplicativo.html', producto=producto)


# Eliminar producto
@app.route('/eliminar_producto/<int:idproducto>')
def eliminar_producto(idproducto):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM producto WHERE idproducto = %s", (idproducto,))
    conn.commit()
    cursor.close()
    flash('Producto eliminado con éxito', 'success')
    return redirect(url_for('listar_productos'))

@app.route('/proveedores')
def listar_proveedores():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM proveedores")
    proveedores = cursor.fetchall()
    cursor.close()
    return render_template('proveedores.html', proveedores=proveedores)

# --------------------------------------------------Proveedores---------------------------------------------------------------------
#---------------------------------------------------Proveedores---------------------------------------------------------------------
@app.route('/agregar_proveedor', methods=['POST'])
def agregar_proveedor():
    if request.method == 'POST':
        idproveedores = request.form['idproveedores']
        nombre = request.form['nombre']
        nit = request.form['nit']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        
        cursor = conn.cursor()
        cursor.execute("INSERT INTO proveedores (idproveedores, nombre, nit, direccion, telefono) VALUES (%s,%s, %s, %s, %s)", (idproveedores,nombre, nit, direccion, telefono))
        conn.commit()
        cursor.close()
        flash('Proveedor agregado con éxito', 'success')
    
    return redirect(url_for('listar_proveedores'))

# Editar un proveedor
@app.route('/editar_proveedor/<int:idproveedores>', methods=['GET', 'POST'])
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
        return redirect(url_for('listar_proveedores'))
    
    return render_template('proveedores/editar_proveedor.html', proveedor=proveedor)

# Eliminar un proveedor
@app.route('/eliminar_proveedor/<int:idproveedores>')
def eliminar_proveedor(idproveedores):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM proveedores WHERE idproveedores = %s", (idproveedores,))
    conn.commit()
    cursor.close()
    flash('Proveedor eliminado con éxito', 'success')
    return redirect(url_for('listar_proveedores'))




if __name__ == "__main__":
    app.run(debug=True)
