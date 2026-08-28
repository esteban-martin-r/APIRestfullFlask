from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User 
from flask_wtf.csrf import CSRFProtect
import controlador   
from auth import auth  
from api.routes import api_bp 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/juegosAlq'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave_super_secreta'

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'

app.register_blueprint(auth, url_prefix='/auth')

app.register_blueprint(api_bp)


@app.route("/")
@app.route("/juegos")
@login_required
def juegos():
    juegos_lista = controlador.obtener_juegos()
    return render_template("juegos.html", juegos=juegos_lista)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/agregar_juego")
@login_required
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
@login_required
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador.insertar_juego(nombre, descripcion, precio)
    return redirect("/juegos")

@app.route("/eliminar_juego", methods=["POST"])
@login_required
def eliminar_juego():
    id_juego = int(request.form["id"])
    controlador.eliminar_juego(id_juego)
    return redirect("/juegos")

@app.route("/formulario_editar_juego/<int:id>")
@login_required
def editar_juego(id):
    juego = controlador.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)

@app.route("/actualizar_juego", methods=["POST"])
@login_required
def actualizar_juego():
    id_juego = int(request.form["id"])
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador.actualizar_juego(id_juego, nombre, descripcion, precio)
    return redirect("/juegos")

if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()     
    app.run(debug=True)
