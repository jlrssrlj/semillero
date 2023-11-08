from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
import psycopg2
from psycopg2 import extras
import json
from flask_session import Session

caja_bp = Blueprint('caja', __name__)

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



@caja_bp.route('/caja', methods =['GET'])
@proteger_ruta
def listar_productos():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('SELECT idcliente,nombrecliente FROM cliente')
    clientes = [row['nombrecliente'] for row in cur.fetchall()]

    cur.execute('SELECT idproducto,nombreproducto FROM producto')
    productos = [row['nombreproducto'] for row in cur.fetchall()]

    return render_template('caja.html', clientes=clientes, productos=productos)
