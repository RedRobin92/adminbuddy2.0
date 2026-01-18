import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'adminbuddy.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    moneda = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    concepto = db.Column(db.String(200), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_view():
    return render_template('login.html')

@app.route('/register')
def register_view():
    return render_template('register.html')

@app.route('/handle_register', methods=['POST'])
def handle_register():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    email = request.form.get('email')
    moneda = request.form.get('moneda')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        return "Las contraseñas no coinciden. <a href='/register'>Vuelve a intentar</a>"
    
    nuevo_usuario = User(
        nombre=nombre,
        apellido=apellido,
        email=email,
        moneda=moneda,
        password=password
    )

    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
        return "Registro exitoso. <a href='/Login'>Iniciar sesión</a>"
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return "Error en el registro. Es posible que ya te hayas registrado con ese correo. <a href='/register'>Vuelve a intentar</a>"

@app.route('/handle_login', methods=['POST'])
def handle_login():
    return "Backend recibio los datos de login."

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Archivo adminbuddy.db verificado/creado correctamente.")

        app.run(debug=True)