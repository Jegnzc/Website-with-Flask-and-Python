from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import secrets

secret = secrets.token_urlsafe(32)


app = Flask(__name__)
app.config['MYSQL_HOST'] = '192.168.0.101'
app.config['MYSQL_USER'] = 'usuario'
app.config['MYSQL_PASSWORD'] = 'jm'
app.config['MYSQL_DB'] = 'umg_didactica'
app.secret_key = secret
mysql = MySQL(app)

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/index.html')
def index_2():
    return render_template('index.html')

@app.route('/docs.html')
def docs():
    return render_template('docs.html')

@app.route('/features.html')
def features():
    return render_template('features.html')

@app.route('/ingresa.html')
def ingresa():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empleados')
    datos = cur.fetchall()
    print(datos)
    return render_template('ingresa.html', empleados = datos)

@app.route('/add_empleado', methods=['POST'])
def add_empleado():
    if  request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        cur = mysql.connection.cursor()
        query = "INSERT INTO empleados (IdNumero, Nombre, Correo, Cumpleaños) VALUES (%s, %s, %s, %s)"
        values = (id, name, email, date)
        cur.execute(query, values)
        mysql.connection.commit()
        flash('Enviado correctamente')
        print(cur.rowcount, "insertado")
        return redirect(url_for('ingresa'))
        
@app.route('/editar/<string:id>')
def obtener_empleado(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empleados WHERE IdPk = {0}'.format(id))
    dato = cur.fetchall()
    return render_template('editar.html', empleado = dato[0])

@app.route('/update/<string:id>', methods = ['POST'])
def actualizar_empleado(id):
    if request.method == 'POST':
        clave = request.form['id']
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        print(clave, name, email,date)
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE empleados
            SET IdNumero = %s,
                Nombre = %s,
                Correo = %s,
                Cumpleaños = %s
            WHERE IdPK = %s
        """, (clave, name, email, date, id))
        mysql.connection.commit()
        flash('Actualizado correctamente')
        return redirect(url_for('ingresa'))

@app.route('/eliminar/<string:id>')
def delete_empleado(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM empleados WHERE IdPk = {0}'.format(id))
    mysql.connection.commit()
    flash('Empleado removido')
    return redirect(url_for('ingresa'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)