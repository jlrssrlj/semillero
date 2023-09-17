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
DB_PASS = "DiegoRuiz5605@!"

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

@app.route('/login/')
def login():
    return render_template('/login.html')

    
@app.route('/hacer_login', methods=['POST'])
def hacer_login():
    conn = connect_to_database()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        correo = request.form['username']
        password = request.form['password']
        
        cursor.execute('SELECT * FROM Login WHERE correo = %s AND password =%s', (correo, password))
        account = cursor.fetchone()

        if account:
            password_rs = account['password']
            print(password_rs)
           
            session['loggedin'] = True
            session['id'] = account['id']
            session['correo'] = account['correo']
            
            return redirect(url_for('prueba'))
        else:
            
            flash('Correo o Contraseña incorrecto')
    else:
        
        flash('Correo o Contraseña incorrecto')

    return render_template('login.html')


cur = conn.cursor()

# Ruta para la página principal

def index():
    # Obtén los datos de productos desde la base de datos
    cur.execute("SELECT * FROM producto")
    productos = cur.fetchall()
    return render_template('herramienta.html', productos=productos)

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




if __name__ == "__main__":
    app.run(debug=True)
