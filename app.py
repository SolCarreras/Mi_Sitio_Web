import pyodbc

from flask import Flask, render_template,request

app = Flask(__name__)



# Conexión a SQL Server
def conexion_bd():
    return pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-BQLA1M6\\SQLEXPRESS07;DATABASE=MiSitio;Trusted_Connection=yes;')

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
