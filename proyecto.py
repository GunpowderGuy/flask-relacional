from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import models

from flask import Flask, render_template, request
app = Flask(__name__)

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True,
                       future=True, connect_args={'check_same_thread': False})
session = Session(engine)
models.Base.metadata.create_all(engine)


def databaseSetup():
    diego = models.Usuario(
        nombre_usuario="Daigo",
        #fullname="Spongebob Squarepants",
        direcciones=[models.Direccion(linea1="Direc", distrito="san borja"),
                     models.Direccion(linea1="Direc1", distrito="sin borja")
                     ],
    )

    maria = models.Usuario(
        nombre_usuario="Maria",
        #fullname="Spongebob Squarepants",
        direcciones=[models.Direccion(linea1="Direc2", distrito="san borja2"),
                     models.Direccion(linea1="Direc12", distrito="sin borja2")
                     ],
    )

    session.add(diego)
    session.add(maria)
    session.commit()

    orden1 = models.Orden(
        costo=3,
        usuarios=[maria]
    )

    session.add(orden1)
    session.commit()


def test1():

    for user in models.getUsuario("Daigo", session):
        print(user)

        print("principio")
        print("s")

        for user in models.getDirecciones(diego, session):
            print(user)

        print("final")

        for user in models.DireccionesDistrito(diego, "san borja", session):
            print(user)

        models.coUsuarios(33, [diego, maria], session)

        for user in models.mayorA(40, session):
            print(user)

        print("penultimo")

        for user in models.UsuariosqueOrdenaron(orden1.id, session):
            print(user)

        print("cierre")


test1()


@app.route("/direcciones/<string:user>")
def direcciones(user):
    usuarioB = models.getUsuario(user, session)
    var1 = next(iter(usuarioB))
    var = models.getDirecciones(var1, session)
    return ''.join(str(x) for x in var)


@app.route("/direccionesdistrito/<string:user>/<string:district>")
def direccionesdistrito(user, district):
    usuarioB = models.getUsuario(user, session)
    var1 = next(iter(usuarioB))
    var = models.DireccionesDistrito(var1, district, session)
    return ''.join(str(x) for x in var)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/nuevaDireccion', methods=['POST'])
def nuevaDireccion1():
    # return str(request.form['nombref'])
    obj = models.Direccion(
        linea1=request.form['direccion_linea1'],
        distrito=request.form['direccion_distrito'],
        referencia_usuario=request.form['nombref']
    )
    session.add(obj)
    session.commit
    return 'comiteado'


@app.route('/nuevaDireccion', methods=['GET'])
def nuevaDireccion():
    # return render_template('shortenurl.html', shortcode=request.form['shortcode'])
    return render_template('ingresarDireccion.html')
