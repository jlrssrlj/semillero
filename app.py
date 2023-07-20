from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

app = Flask(__name__)

app.secret_key = "prueba"

DB_HOST = "localhost"
DB_NAME = "semillero"
DB_USER = "ted127"
DB_PASS = "1273458"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def index2():
    return render_template('index.html')

@app.route('/Login.html')
def Login():
    return render_template('Login.html')    

# Ruta para mostrar el formulario de inicio de sesión
@app.route('/login', methods=['GET'])
def mostrar_formulario():
    return render_template('login.html')

# Ruta para manejar el inicio de sesión
@app.route('/hacer_login', methods=['POST'])
def login():
    correo = request.form.get('Correo')
    password = request.form.get('pass')

    if not correo or not password:
        return jsonify({'message': 'Correo y contraseña son campos requeridos'}), 400

    connection = None
    cursor = None
    try:
        # Establecer conexión a la base de datos
        connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Consultar la base de datos para obtener el hash de la contraseña
        query = "SELECT * FROM login WHERE correo = %s"
        cursor.execute(query, (correo,))
        employee = cursor.fetchone()

        if employee:
            hashed_password = employee['Password']

            if check_password_hash(hashed_password, password):
                session['loggedin'] = True
                session['id'] = employee['Idempleado']
                session['Correo'] = employee['Correo']
                return jsonify({'message': 'Inicio de sesión exitoso'})
            else:
                return jsonify({'message': 'Correo o contraseña incorrectos'}), 401
        else:
            return jsonify({'message': 'Correo o contraseña incorrectos'}), 401

    except Exception as e:
        return jsonify({'message': 'Error al procesar la solicitud', 'error': str(e)}), 500
    finally:
        # Cerrar la conexión y el cursor en caso de que existan
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    app.run(debug=True)
