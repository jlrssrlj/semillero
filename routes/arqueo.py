from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from conection import get_db_connection
import json
from flask_session import Session

arqueo_bp = Blueprint('arqueo', __name__)


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

#Mostrar la tabla de arqueo
@arqueo_bp.route('/arqueo')
def listar_arqueo():
    
    s = "SELECT * FROM arqueos"
    cur.execute(s)
    list_users = cur.fetchall()
    return render_template('arqueo.html',  list_users= list_users)

# Agregar Caja
@arqueo_bp.route('/agregar_arqueo', methods=['POST'])
def agregar_arqueo():
    if request.method == 'POST':
        monto = request.form['monto'] 
        apertura = request.form['apertura']
        cierra = request.form['cierre']
        idempleado = request.form['idempleado']
 
        cur.execute("INSERT INTO arqueos (monto, apertura, cierre, idempleado) VALUES (%s, %s, %s, %s)", (monto, apertura, cierra, idempleado))
        mydb.commit()
        cur.close()
    return redirect(url_for('arqueo.listar_arqueo'))

#Actualizar arqueo


# Editar arqueo
@arqueo_bp.route('/editar_arqueo/<id>')
def get_contact(id):
    try:  
        
        cur.execute('SELECT*FROM arqueos WHERE idarqueo=%s', (int(float(id)),))
        data=cur.fetchall()
        return render_template('edit_arqueo.html', arqueo=data[0])
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

@arqueo_bp.route('/actualizarARQ/<id>', methods=["POST"])
def update_contact(id):
    try: 
        if request.method == 'POST':
            monto = request.form['monto'] 
            apertura = request.form['apertura']
            cierra = request.form['cierra']
            idempleado = request.form['idempleado']
            
            cur.execute(""" UPDATE arqueos SET monto=%s, apertura=%s, cierra=%s, idempleado=%s  WHERE idarqueo=%s""", (monto, apertura, cierra, idempleado, id))
            mydb.commit()
            return redirect(url_for('arqueo.listar_arqueo')) 
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500
    
#Eliminar arqueo

@arqueo_bp.route('/eliminar_arqueo/<int:idarqueo>')
def eliminar_arqueo(idarqueo):
    try:
        
        cur.execute("DELETE FROM arqueos WHERE idarqueo = %s", (idarqueo,))
        mydb.commit()
        cur.close()
        return redirect(url_for('listar_arqueo'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500