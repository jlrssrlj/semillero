from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify, sessions, url_for
from routes.productos import productos_bp
from routes.proveedores import proveedores_bp
from routes.empleado import empleado_bp
from routes.clientes import cliente_bp
from routes.arqueo import arqueo_bp
from routes.ventas import ventas_bp
from flask_session import Session
import json
from conection import get_db_connection


app = Flask(__name__)
app.secret_key = 'semillero'

mydb = get_db_connection()

app.register_blueprint(productos_bp)
app.register_blueprint(proveedores_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(empleado_bp)
app.register_blueprint(arqueo_bp)
app.register_blueprint(ventas_bp)


def proteger_ruta(func):
    def wrapper(*args, **kwargs):
        if 'logueado' in session and session['logueado']:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    wrapper.__name__ = func.__name__
    return wrapper

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/salir')
def salir():
    session.pop('logueado', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/caja')
@proteger_ruta
def caja():
    return render_template('caja.html')

@app.route('/hacer_login', methods=["POST", "GET"])
def hacer_login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        correo = request.form['username']
        password = request.form['password']
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM empleados WHERE usuario = %s AND clave = %s', (correo, password))
        account = mycursor.fetchone()

        if account:
            session['logueado'] = True
            session['username'] = correo
            return redirect(url_for('productos.listar_productos'))
        else:
            flash('Credenciales incorrectas. Inténtalo de nuevo.', 'error')
            return render_template("login.html")

    return render_template('login.html')

def paginanoencontrada(error):
    return "<h1>La página que intenta encontrar no existe<h1>", 404

if __name__ == "__main__":
    app.register_error_handler(404, paginanoencontrada)
    app.run(debug=True, port=5500)