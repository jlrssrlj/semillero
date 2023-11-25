from flask import Blueprint, flash, render_template, request, redirect, url_for, jsonify, session
from conection import get_db_connection
import datetime
from proteger import proteger_ruta
import locale

locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')

arqueocajero = Blueprint('arqueocajero', __name__)

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
            
            list_users_formatted = [(user[0], locale.currency(user[1], grouping=True), user[2], user[3],user[4],user[5],user[6]) for user in list_users]

            return render_template('cajero/arqueocajero.html', list_users=list_users_formatted)

    except Exception as ex:
        flash(f"Error: {str(ex)}", 'error')
        return redirect(url_for('arqueocajero.listar_arqueo'))

@arqueocajero.route('/agregar_arqueocajero', methods=['POST'])
def agregar_arqueo():
    try:
        if request.method == 'POST':
            cur = mydb.cursor()
            idempleado = session.get('idempleado', None)

            if idempleado is not None:
                monto = request.form['monto']                
                session['monto'] = int(monto)
                apertura = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cierra = None  

                cur.execute("INSERT INTO arqueos (monto, apertura, cierre, idempleado) VALUES (%s, %s, %s, %s)", (monto, apertura, cierra, idempleado))
                mydb.commit()
                session['monto'] = float(monto)
                cur.close()
                # Obtener el ID del arqueo recién insertado
                id_arqueo = cur.lastrowid

                # Almacenar el idarqueo en la sesión
                session['idarqueo_actual'] = id_arqueo

                return redirect(url_for('arqueocajero.listar_arqueo'))   
        
        return render_template('cajero/arqueocajero.html')
    except Exception as ex:
       flash(f"Error: {str(ex)}", 'error')
       return redirect(url_for('arqueocajero.listar_arqueo'))
    
@arqueocajero.route('/editar_arqueocajero/<id>')
def get_contact(id):
    try:  
        cur = mydb.cursor()
        cur.execute('SELECT*FROM arqueos WHERE idarqueo=%s',  (int(float(id)),))
        data=cur.fetchall()
        return render_template('cajero/cierrecajero.html', arqueo=data[0])
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500
    

@arqueocajero.route('/actualizar_arqueoqueocajero/<int:idarqueo>', methods=['POST'])
def actualizar_arqueo(idarqueo):
    #try:
        if request.method == 'POST':
            cur = mydb.cursor()
            total_ventas = session.get('total_ventas')
            total_gastos = session.get('total_gastos')
            monto = session.get('monto')
            # Calcular el monto segun sitema
            total = monto + total_ventas - total_gastos
            montocierre = float(request.form['montocierre'])
            diferencia = montocierre-total
            # Capturar la fecha y hora actual al momento del cierre
            cierra = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            idempleado = session.get('idempleado', None)
            print("ventas",total_ventas)
            print("gastos",total_gastos)
            print("apertura",monto)
            print("diferencia:", diferencia)
            cur.execute("UPDATE arqueos SET montocierre=%s, cierre=%s, idempleado=%s,diferencia=%s WHERE idarqueo=%s", (montocierre, cierra, idempleado,diferencia, idarqueo))
            mydb.commit()
            cur.close()
        return redirect(url_for('arqueocajero.listar_arqueo'))
    #except Exception as ex:
     #   return jsonify({'mensaje': f"Error: {str(ex)}"}), 500



