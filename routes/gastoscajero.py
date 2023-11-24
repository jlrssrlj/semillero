from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from conection import get_db_connection
from proteger import proteger_ruta
import locale

locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')

mydb = get_db_connection()

gastoscajero = Blueprint('gastoscajero', __name__)

@gastoscajero.route('/gastoscajero', methods=['GET'])
@proteger_ruta
def listar_gastos():
    try:
        with mydb.cursor() as cur:
            cur.execute("SELECT * FROM gastos ORDER BY idgastos ASC")
            # Convertir cada fila en un diccionario
            columns = [column[0] for column in cur.description]
            gastos = [dict(zip(columns, row)) for row in cur.fetchall()]

        # Calcular el total de gastos
        total_gastos = sum(gasto['valor'] for gasto in gastos)

        # Guardar el total en la sesión
        session['total_gastos'] = total_gastos

        return render_template('cajero/gastoscajero.html', gastos=gastos,total_gastos=total_gastos)
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


@gastoscajero.route('/agregar_gastoscajero', methods=['POST'])
def agregar_gastos():
    #try:
        if request.method == 'POST':
            factura = request.form['factura']
            valor = request.form['valor']
            nombreproveedor = request.form['nombreproveedor']
            pago = request.form['pago']
            idproveedores = request.form['idproveedores']
            
            # Manejar el caso en que 'idarqueo_actual' no esté presente en la sesión
            idarqueo = session.get('idarqueo_actual')
            if idarqueo is None:
                flash("No hay un id de arqueo actual en la sesión.", 'error')
                return redirect(url_for('arqueocajero.arqueocajero.html'))
            
            with mydb.cursor() as cursor:
                cursor.execute("INSERT INTO gastos (factura, valor, nombreproveedor, pago, idproveedores, idarqueo) VALUES (%s, %s, %s, %s, %s, %s)",
                               (factura, valor, nombreproveedor, pago, idproveedores, idarqueo))
            mydb.commit()

        return redirect(url_for('gastoscajero.listar_gastos'))
    #except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

@gastoscajero.route('/obtener_total_gastos', methods=['GET'])
def obtener_total_gastos():
    try:
        # Recuperar el total de gastos desde la sesión
        total_gastos = session.get('total_gastos', 0)
        return jsonify({'total_gastos': total_gastos})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500