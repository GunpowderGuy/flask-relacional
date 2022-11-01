#https://docs.sqlalchemy.org/en/14/orm/quickstart.html
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Table

Base = declarative_base()

class Usuario(Base):
    __tablename__="usuario"
    nombre_usuario = Column(String(30), primary_key= True)
    direcciones = relationship("Direccion", backref="usuario")
    
    def __str__(self):
       return "okay"


class Direccion(Base):
    __tablename__="direccion"
    linea1 = Column(String(8), nullable=False, primary_key=True)
    #linea2 = Column(String(8), nullable=True, primary_key=True)
    distrito = Column(String(10))
    referencia_usuario = Column(String(30),ForeignKey("usuario.nombre_usuario"))
    
    def __str__(self):
       return str(self.linea1) + "  " + str(self.distrito) + " "
       

association_table = Table(
    "association",
    Base.metadata,
    Column("left_id", ForeignKey("usuario.nombre_usuario")),
    Column("right_id", ForeignKey("orden.id")),
)


class Orden(Base):
    __tablename__ = "orden"
    id = Column(Integer,primary_key = True)
    fecha_creacion = Column(Date, index=True)
    costo = Column(Integer)
    usuarios = relationship("Usuario", secondary=association_table)

from sqlalchemy import select

def getUsuario(nom, session):
     stmt = select(Usuario).where(Usuario.nombre_usuario.in_([nom]))
     return session.scalars(stmt)

def getDirecciones(usuarioO,sessioN):
    return sessioN.scalars(select(Direccion).where(Direccion.referencia_usuario.in_([usuarioO.nombre_usuario])))

def DireccionesDistrito(usuarioO, distritO,sessioN):
    return sessioN.scalars(select(Direccion).where(Direccion.referencia_usuario.in_([usuarioO.nombre_usuario]))
    .where(Direccion.distrito == distritO))

def coUsuarios(monto,usuarioS,sessio):
    ord = Orden(costo=monto,usuarios=usuarioS)
    sessio.add(ord)
    sessio.commit

def Usarios(id_orden,sessio):
    sessio.scalars(select(Orden).where(Orden.id == id_orden))

def UsuariosqueOrdenaron(id_orden,sessio):
    objeto = sessio.scalars(select(Orden).where(Orden.id == id_orden))
    return objeto.first().usuarios

def mayorA(monto,sessio):
    return sessio.scalars(select(Orden).where(Orden.costo > monto ))