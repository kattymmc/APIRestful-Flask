from flask.app import Flask
from flask import jsonify
from flask.globals import request, session
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_bcrypt import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'ThisIsASecretKey'

## CONFIGURACION DE LA BD
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)
bcrypt = Bcrypt(app)

# http://localhost:5000/
@app.route('/')
def inicio():
    app.logger.debug('Mensaje a nivel debug')
    app.logger.info(f'Entramos al path {request.path}')
    app.logger.warn('Mensaje a nivel error') # solo se esté activa en produccion
    if 'username' in session:
        return render_template('inicio.html', username=session["username"])
    return 'No ha hecho login'

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # obtiene el input de name 'username'
        usuario = request.form['username']
        contrasena = request.form['password']
        cursor = mysql.connection.cursor()
        qry = "SELECT contrasena FROM usuarios WHERE usuario = '{}'".format(usuario)
        cursor.execute(qry)
        account = cursor.fetchone()
        app.logger.warn(account)
        # agregar usuario a la sesión
        if check_password_hash(account[0],contrasena):
            session['username'] = usuario
        else:
            return 'Usuario/contraseña Incorrectos!'
        return redirect(url_for('inicio'))
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        mentor = request.form['mentor']
        mentorizado = request.form['mentorizado']
        carrera = request.form['carrera']
        #telefono = request.form['telefono']
        #area = request.form['area']
        #usuario = request.form['username']
        #contrasena = request.form['contrasena']
        #contrasena = generate_password_hash(contrasena).decode('utf8')
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO info VALUES(NULL,%s,%s,%s)''', (mentor,mentorizado,carrera))
        mysql.connection.commit()
        cursor.close()
        return "User added"
        #return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/info', methods=['GET'])
def obtenerInfo():
    cursor = mysql.connection.cursor()
    qry = "SELECT mentor,mentorizado,carrera FROM info"
    cursor.execute(qry)
    users_info = cursor.fetchall()
    app.logger.warn(users_info)
    return render_template('info.html', info=users_info)

# Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('inicio'))

@app.route('/saludar/<nombre>')
def saludar(nombre):
    return f'Saludos {nombre.upper()}'

## Si el parametro no es string, se debe especificar el tipo
@app.route('/edad/<int:edad>')
def mostrar_edad(edad):
    return f'Tu edad es: {edad + 1}'

## Peticiones POST
@app.route('/mostrar/<nombre>', methods=['GET','POST'])
def mostrar_nombre(nombre):
    ## Renderizar Template, pasar variables
    return render_template('mostrar.html', nombre=nombre)

## Redirecionar a una URL: redirect(url_for(nombre_funcion, parametros))
@app.route('/redireccionar')
def redireccionar():
    return redirect(url_for('mostrar_nombre', nombre='Kattymmc'))

## Manejo de errores
@app.route('/salir')
def salir():
    return abort(404)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('error404.html', error=error), 404

## API REST: Retornar JSON
@app.route('/api/mostrar/<nombre>', methods=['GET','POST'])
def mostrar_json(nombre):
    valores = {'nombre': nombre, 'metodo_http': request.method }
    ## Si se retorna un objeto, se debe utilizar jsonify(valores)
    return valores

@app.route('/api/usuarios')
def mostrar_usuarios():
    cursor = mysql.connection.cursor()
    qry = "SELECT nombres,apellidos,correo,telefono,area FROM usuarios"
    cursor.execute(qry)
    users = cursor.fetchall()
    return jsonify(users)


# correr: flask run
# correr en desarollo
# set FLASK_APP=app.py
# set FLASK_ENV=development