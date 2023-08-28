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
DB_PASS = "1273458mN"

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

@app.route('/login')
def index():
    return render_template('index.html')


    
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



if __name__ == "__main__":
    app.run(debug=True)
