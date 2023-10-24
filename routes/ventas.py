from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
import psycopg2
from psycopg2 import extras
import json
from flask_session import Session

ventas_bp = Blueprint('ventas', __name__)


with open('appsettings.json') as config_file:
    config = json.load(config_file)

db_url = config.get('DefaultConnection')


conn = psycopg2.connect(db_url)

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
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        s = "SELECT v.idventa, p.nombreproducto, p.precio, v.pago, c.nombrecliente, e.nombreempleado, v.horainicial FROM venta v inner JOIN empleado e ON v.idempleado = e.idempleado INNER JOIN cliente c ON v.idcliente = c.idcliente INNER JOIN producto p ON v.idproducto = p.idproducto"
        cur.execute(s)
        list_users = cur.fetchall()
        return render_template('ventas.html', list_users=list_users)
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500