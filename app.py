from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
import psycopg2
import psycopg2.extras


app = Flask(__name__)

app.secret_key = "prueba"
bcrypt = Bcrypt(app)

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.office365.com'  # Servidor SMTP (por ejemplo, Gmail)
app.config['MAIL_PORT'] = 587  # Puerto del servidor SMTP
app.config['MAIL_USE_TLS'] = True  # Usar TLS para la conexión
app.config['MAIL_USERNAME'] = 'ramos014@hotmail.com'  # Tu dirección de correo
app.config['MAIL_PASSWORD'] = 'Jorgeramos123.'  # Tu contraseña de correo

mail = Mail(app)

@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        recipient = request.form['recipient']
        subject = request.form['subject']
        message_body = request.form['message_body']
        
        msg = Message(subject=subject, recipients=[recipient])
        msg.body = message_body
        
        try:
            mail.send(msg)
            flash('Correo enviado exitosamente', 'success')
        except Exception as e:
            flash(f'Error al enviar el correo: {e}', 'danger')
        
        return redirect(url_for('send_email'))
    
    return render_template('index.html')

#Configuracion base de datos
DB_HOST = "localhost"
DB_NAME = "semillero"
DB_USER = "postgres"
DB_PASS = "Srljjlrs2023*"

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
