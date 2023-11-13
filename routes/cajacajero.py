from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from conection import get_db_connection
import datetime
from proteger import proteger_ruta
from flask_session import Session


cajacajero = Blueprint('cajacajero', __name__)

# Obtener la conexión de la base de datos y el cursor
mydb = get_db_connection()