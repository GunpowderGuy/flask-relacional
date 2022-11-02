import models
from flask import render_template

from flask import Flask

app = Flask(__name__)

from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True,connect_args={'check_same_thread': False})

from sqlalchemy.orm import Session
session = Session(engine)

models.Base.metadata.create_all(engine)


diego = models.Usuario(
         nombre_usuario="Daigo",
         #fullname="Spongebob Squarepants",
         direcciones=[models.Direccion(linea1="Direc",distrito="san borja"),
         models.Direccion(linea1="Direc1",distrito="sin borja")
         ],
     )

maria = models.Usuario(
         nombre_usuario="Maria",
         #fullname="Spongebob Squarepants",
         direcciones=[models.Direccion(linea1="Direc2",distrito="san borja2"),
         models.Direccion(linea1="Direc12",distrito="sin borja2")
         ],
     )

session.add(diego)
session.add(maria)
session.commit()

orden1 = models.Orden(
  costo = 3,
  usuarios = [maria]
)

session.add(orden1)
session.commit()


from models import Direccion, DireccionesDistrito, Usuario, coUsuarios, getDirecciones, getUsuario, mayorA

def test1():

    for user in getUsuario("Daigo",session):
        print(user)
        
        print("principio")
        print("s")   

        for user in getDirecciones(diego,session):
            print(user)


        print("final")

        #print(DireccionesDistrito(diego,"san borja"))

        for user in models.DireccionesDistrito(diego,"san borja",session):
            print(user)
        
        coUsuarios(33,[diego,maria],session)

        for user in mayorA(40,session):
            print(user)
        
        print("penultimo")

        for user in models.UsuariosqueOrdenaron(orden1.id,session):
            print(user)

        print("cierre")

test1()


@app.route("/direcciones/<string:user>")
def direcciones(user):
    usuarioB = getUsuario(user,session)
    var1 = next(iter(usuarioB))
    var = getDirecciones(var1,session)
    return ''.join(str(x) for x in var)


@app.route("/direccionesdistrito/<string:user>/<string:district>")
def direccionesdistrito(user,district):
    usuarioB = getUsuario(user,session)
    var1 = next(iter(usuarioB))
    var = models.DireccionesDistrito(var1,district,session)
    return ''.join(str(x) for x in var)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

from flask import Flask, render_template, request

@app.route('/nuevaDireccion', methods=['POST'])
def nuevaDireccion1():
    #return render_template('shortenurl.html', shortcode=request.form['shortcode'])
    
    return str(request.form['nombref'])

@app.route('/nuevaDireccion', methods=['GET'])
def nuevaDireccion():
    #return render_template('shortenurl.html', shortcode=request.form['shortcode'])
    return render_template('ingresarDireccion.html')