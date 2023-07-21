from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
import psycopg2
import psycopg2.extras


app = Flask(__name__)

app.secret_key = "prueba"
bcrypt = Bcrypt(app)



DB_HOST = "localhost"
DB_NAME = "semillero"
DB_USER = "ted127"
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

@app.route('/index.html')
def index2():
    return render_template('index.html')

@app.route('/Login.html')
def Login():
    return render_template('Login.html')    

@app.route('/prueba.html')
def prueba():
    return render_template('prueba.html')   
    


@app.route('/hacer_login', methods=['POST'])
def hacer_login():
    conn = connect_to_database()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        correo = request.form['username']
        password = request.form['password']
        print(password)

        # Check if account exists using PostgreSQL
        cursor.execute('SELECT * FROM Login WHERE correo = %s AND password =%s', (correo, password))
        # Fetch one record and return result
        account = cursor.fetchone()

        if account:
            password_rs = account['password']
            print(password_rs)
           
            session['loggedin'] = True
            session['id'] = account['id']
            session['correo'] = account['correo']
            # Redirect to home page
            return redirect(url_for('prueba'))
        else:
            # Incorrect password
            flash('Incorrect username/password')
    else:
        # Incorrect username or account doesn't exist
        flash('Incorrect username/password')

    return render_template('login.html')



if __name__ == "__main__":
    app.run(debug=True)
