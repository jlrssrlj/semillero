from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from conection import get_db_connection
from proteger import proteger_ruta
from flask_session import Session

mydb = get_db_connection()

gastoscajero = Blueprint('gastoscajero', __name__)



@gastoscajero.route('/gastoscajero', methods=['GET'])
@proteger_ruta
def listar_gastos():
    try:
        with mydb.cursor() as cur:
            cur.execute("SELECT * FROM gastos ORDER BY idgastos ASC")
            gastos = cur.fetchall()
        return render_template('cajero/gastoscajero.html', gastos=gastos)
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


def obtener_proveedores():
    cur = mydb.cursor()
    cur.execute("SELECT nombrepro FROM proveedores")
    proveedores = cur.fetchall()
    cur.close()
    return proveedores

@gastoscajero.route('/mostrar_formulario_gastos', methods=['GET'])
def mostrar_formulario_gastos():
    print("Llamando a mostrar_formulario_gastos")  # Agrega esta línea
    proveedores = obtener_proveedores()
    return render_template('cajero/gastoscajero.html', proveedores=proveedores)


@gastoscajero.route('/agregar_gastoscajero', methods=['POST'])
def agregar_gastos():
    try:
        if request.method == 'POST':
            factura = request.form['factura']
            valor = request.form['valor']
            nombreproveedor = request.form['nombrepro']
            pago = request.form['pago']
            idproveedores = request.form['idproveedores']
            idarqueo = request.form['idarqueo']
            with mydb.cursor() as cursor:
                cursor.execute("INSERT INTO gastos (factura, valor, nombrepro, pago, idproveedores, idarqueo) VALUES (%s, %s, %s, %s, %s,%s)",
                               (factura, valor, nombreproveedor, pago, idproveedores, idarqueo))
            mydb.commit()
        return redirect(url_for('gastoscajero.listar_gastos'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500




