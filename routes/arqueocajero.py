from flask import Blueprint, flash, render_template, request, redirect, url_for, jsonify, session
from conection import get_db_connection
import datetime
from proteger import proteger_ruta
from flask import session
import locale


locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')



arqueocajero = Blueprint('arqueocajero', __name__)

# Obtener la conexión de la base de datos y el cursor
mydb = get_db_connection()




@arqueocajero.route('/arqueocajero')
@proteger_ruta
def listar_arqueo():
    try:
        cur = mydb.cursor()
        idempleado = session.get('idempleado', None)

        if idempleado is not None:
            s = "SELECT * FROM arqueos WHERE idempleado = %s"
            cur.execute(s, (idempleado,))
            list_users = cur.fetchall()
            cur.close()
            
            list_users_formatted = [(user[0], locale.currency(user[1], grouping=True), user[2], user[3]) for user in list_users]

            return render_template('cajero/arqueocajero.html', list_users=list_users_formatted)
    
    except Exception as ex:
        flash(f"Error: {str(ex)}", 'error')
        return redirect(url_for('arqueocajero.listar_arqueo'))

    

    
   
    return render_template('cajero/arqueocajero.html')

@arqueocajero.route('/agregar_arqueocajero', methods=['POST'])
def agregar_arqueo():
    try:
        if request.method == 'POST':
            cur = mydb.cursor()

            # Obtener el ID del empleado de la sesión actual
            idempleado = session.get('idempleado', None)

            if idempleado is not None:
                monto = request.form['monto']
                # Capturar la fecha y hora actual al momento de la apertura
                apertura = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cierra = None  

                cur.execute("INSERT INTO arqueos (monto, apertura, cierre, idempleado) VALUES (%s, %s, %s, %s)", (monto, apertura, cierra, idempleado))
                mydb.commit()
                return redirect(url_for('arqueocajero.listar_arqueo'))   
        
        return render_template('cajero/arqueocajero.html')
    except Exception as ex:
       flash(f"Error: {str(ex)}", 'error')
       return redirect(url_for('arqueocajero.listar_arqueo'))


