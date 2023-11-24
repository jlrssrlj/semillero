from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from proteger import proteger_ruta
from flask_session import Session
from conection import get_db_connection

ventas_bp = Blueprint('ventas', __name__)


mydb = get_db_connection()
cur = mydb.cursor()

def proteger_ruta(func):
    def wrapper(*args, **kwargs):
        if 'logueado' in session and session['logueado']:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    wrapper.__name__ = func.__name__
    return wrapper

# --------------------------------------------TABLA DE VENTAS-------------------------------------------------

@ventas_bp.route('/ventas')
@proteger_ruta
def listar_empleado():
    try:
        # Obtener el idempleado de la sesión
        idempleado = session.get('idempleado', None)

        # Verificar que el idempleado está presente en la sesión
        if idempleado is None:
            return jsonify({'mensaje': 'No se proporcionó el idempleado en la sesión.'}), 400

        # Consulta SQL para obtener las ventas por idempleado
        s = "SELECT v.idventa, p.nombreproducto, p.precio, v.pago, c.nombrecliente, e.nombreempleado, v.horainicial FROM ventas v INNER JOIN empleados e ON v.idempleado = e.idempleado INNER JOIN clientes c ON v.idcliente = c.idcliente INNER JOIN productos p ON v.idproducto = p.idproducto WHERE e.idempleado = %s ORDER BY v.horainicial DESC"
        cur.execute(s, (idempleado,))

        # Obtener los nombres de las columnas
        columns = [column[0] for column in cur.description]

        # Convertir cada fila en un diccionario
        list_users = [dict(zip(columns, row)) for row in cur.fetchall()]

        # Calcular el total de ventas por idempleado
        total_ventas = sum(venta['precio'] for venta in list_users)

        # Guardar el total en la sesión
        session['total_ventas'] = total_ventas

        # Cerrar la conexión después de realizar todas las operaciones
        cur.close()

        return render_template('ventas.html', list_users=list_users)
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


