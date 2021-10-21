'''from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABAE_URI'] = 'mysql+pymsql://root@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)'''

'''class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    correo = db.Column(db.String(70), unique=True)
    telefono = db.Column(db.String(10))
    area = db.Column(db.String(30))
    usuario = db.Column(db.String(70), unique=True)
    contrasena = db.Column(db.String(70))'''