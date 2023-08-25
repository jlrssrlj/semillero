from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.office365.com'  # Servidor SMTP (por ejemplo, Gmail)
app.config['MAIL_PORT'] = 587  # Puerto del servidor SMTP
app.config['MAIL_USE_TLS'] = True  # Usar TLS para la conexión
app.config['MAIL_USERNAME'] = 'jorge.ramos-s@hotmail.com'  # Tu dirección de correo
app.config['MAIL_PASSWORD'] = 'Jorgeramos123.'  # Tu contraseña de correo

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.run(debug=True)
