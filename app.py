from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras

app=Flask(__name__)

app.secret_key= "prueba"

DB_HOST="localhost"
DB_NAME="prueba"
DB_USER="ted127"
DB_PASS="1273458"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/')
def index():
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s="SELECT * FROM login"
    cur.execute(s)
    list_users =cur.fetchall()
    return render_template('index.html',list_users=list_users)



if __name__ == "__main__":
    app.run(debug=True)