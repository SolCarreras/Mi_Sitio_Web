
from flask import Flask, render_template,request

app = Flask(__name__)


# app.py (fragmento)
import os
from dotenv import load_dotenv
import pyodbc

load_dotenv()  # carga .env en entorno (solo en desarrollo)

def conexion_bd():
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    trusted = os.getenv("DB_TRUSTED", "yes").lower()  # yes/no

    if trusted in ("yes", "true", "1"):
        conn_str = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
    else:
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        conn_str = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password};"

    return pyodbc.connect(conn_str)


@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    mensaje = None
    if request.method == 'POST':
        nombre_apellido = request.form['nombre_apellido']
        telefono = request.form['telefono']
        mensaje_formulario = request.form['mensaje']

        conn = conexion_bd()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contacto (nombre_apellido, telefono, mensaje)
            VALUES (?, ?, ?)""",
            nombre_apellido, telefono, mensaje_formulario)
        conn.commit()
        conn.close()

        mensaje = "¡Gracias por contactarte! Pronto nos pondremos en contacto."

    return render_template('contacto.html', mensaje=mensaje)

# Rutas
@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/mis_proyectos')
def mis_proyectos():
    return render_template('mis_proyectos.html')


if __name__ == '__main__':
    app.run(debug=True)
