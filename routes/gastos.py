from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from conection import get_db_connection
from proteger import proteger_ruta
from flask_session import Session

mydb = get_db_connection()

gastos_bp = Blueprint('gastos', __name__)



@gastos_bp.route('/gastos', methods=['GET'])
@proteger_ruta
def listar_gastos():
    try:
        with mydb.cursor() as cur:
            cur.execute("SELECT * FROM gastos ORDER BY idgastos ASC")
            columns = [column[0] for column in cur.description]
            gastos = [dict(zip(columns, row)) for row in cur.fetchall()]
        # Calcular el total de gastos
        total_gastos = sum(gasto['valor'] for gasto in gastos)

        # Guardar el total en la sesión
        session['total_gastos'] = total_gastos
        return render_template('gastos.html', gastos=gastos,total_gastos=total_gastos)
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500
    

# Agregar gastos
@gastos_bp.route('/agregar_gastos', methods=['POST'])
def agregar_gastos():
    try:
        if request.method == 'POST':
            factura = request.form['factura']
            valor = request.form['valor']
            nombreproveedor = request.form['nombreproveedor']
            pago = request.form['pago']
            idproveedores = request.form['idproveedores']
            idarqueo = session.get('idarqueo_actual', None)

            if idarqueo is not None:
                with mydb.cursor() as cursor:
                    cursor.execute("INSERT INTO gastos (factura, valor, nombreproveedor, pago, idproveedores, idarqueo) VALUES (%s, %s, %s, %s,%s, %s)",
                                   (factura, valor, nombreproveedor, pago,idproveedores, idarqueo))
                mydb.commit()
                
                
            return redirect(url_for('gastos.listar_gastos'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500



# Editar gastos
@gastos_bp.route('/editar_gastos/<int:idgastos>')
def get_gastos(idgastos):
    try:
        with mydb.cursor() as cur:
            cur.execute('SELECT * FROM gastos WHERE idgastos = %s', (idgastos,))
            data = cur.fetchone()
        return render_template('edit_gastos.html', gastos=data)
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


@gastos_bp.route('/actualizar_gastos/<int:id>', methods=["POST"])
def update_gastos(id):
    try:
        if request.method == 'POST':
            factura = request.form['factura']
            valor = request.form['valor']
            nombreproveedor = request.form['nombreproveedor']
            pago = request.form['pago']
            idproveedores = request.form['idproveedores']
            with mydb.cursor() as cur:
                cur.execute("""
                    UPDATE gastos
                    SET factura=%s, valor=%s, nombreproveedor=%s, pago=%s, idproveedores=%s
                    WHERE idgastos=%s
                """, (factura, valor, nombreproveedor, pago, idproveedores, id))
            mydb.commit()
            return redirect(url_for('gastos.listar_gastos'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

# Eliminar gastos
@gastos_bp.route('/eliminar_gastos/<int:idgastos>')
def eliminar_gastos(idgastos):
    try:
        with mydb.cursor() as cursor:
            cursor.execute("DELETE FROM gastos WHERE idgastos = %s", (idgastos,))
            mydb.commit()
        return redirect(url_for('gastos.listar_gastos'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500
    
@gastos_bp.route('/obtener_total_gastos', methods=['GET'])
def obtener_total_gastos():
    try:
        # Recuperar el total de gastos desde la sesión
        total_gastos = session.get('total_gastos', 0)
        return jsonify({'total_gastos': total_gastos})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500
