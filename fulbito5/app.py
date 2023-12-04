# Importación de módulos necesarios
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import IntegrityError
import datetime

#Creacion de APP Flask
app = Flask(__name__)
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:manu@localhost/test'
#app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/proyecto'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow

#Definimo el modelo de datos
class Empleado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido= db.Column(db.String(100))
    whatsapp= db.Column(db.String(16))
    posicion= db.Column(db.String(20))
    
    
    def __init__(self,nombre,apellido,whatsapp,posicion):
        self.nombre = nombre
        self.apellido = apellido
        self.whatsapp = whatsapp
        self.posicion = posicion
        

#Definimos el esquema
class EmpleadoSchema(ma.Schema):
    class Meta:
        fields = ('id','nombre','apellido','whatsapp','posicion')


#Crear esquemas para la db
empleado_schema = EmpleadoSchema() #trae un empleado
empleados_schema = EmpleadoSchema(many=True) #Para traer más de un empleado

#Creamos la tablas
with app.app_context():
    db.create_all()

#Endpoint Get
@app.route('/empleados', methods=['GET'])
def get_all_empleados():
    try:
        empleados = Empleado.query.all()
        if empleados:
            return empleados_schema.jsonify(empleados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Endpoint Get by Id
@app.route('/empleados/<id>', methods=['GET'])
def get_empleado(id):
    try:
        empleado = Empleado.query.get(id)

        if empleado:
            return empleado_schema.jsonify(empleado)
        else:
            return jsonify({'error': 'Empleado no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para crear un nuevo empleado mediante una solicitud POST
@app.route('/empleados', methods=['POST'])
def create_empleado():
    try:
        json_data = request.get_json()
        nombre = json_data['nombre']
        apellido = json_data['apellido']
        whatsapp = json_data['whatsapp']
        posicion = json_data['posicion']
        
        #fecha_nacimiento = datetime.datetime.strptime(json_data['fecha_nacimiento'], "%Y-%m-%d").date()

        # Cargar datos JSON en un objeto Empleado
        nuevo_empleado = Empleado(nombre, apellido, whatsapp, posicion)

        # Realizar validaciones adicionales si es necesario

        db.session.add(nuevo_empleado)
        db.session.commit()

        return empleado_schema.jsonify(nuevo_empleado), 201  # Devolver el empleado creado con el código 201 (creado)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400  # Devolver mensajes de error de validación con el código 400 (error de solicitud)

# Ruta para actualizar un empleado mediante una solicitud PUT
@app.route('/empleados/<id>', methods=['PUT'])
def update_empleado(id):
    try:
        empleado = Empleado.query.get(id)

        # Verificar si el empleado existe en la base de datos
        if empleado:
            json_data = request.get_json()
            empleado.nombre = json_data.get('nombre', empleado.nombre)
            empleado.apellido = json_data.get('apellido', empleado.apellido)
            empleado.whatsapp = json_data.get('whatsapp', empleado.whatsapp)
            empleado.posicion = json_data.get('posicion', empleado.posicion)
            
            # Realizar validaciones según tus requerimientos

            db.session.commit()
            return empleado_schema.jsonify(empleado)
        else:
            return jsonify({'error': 'Empleado no encontrado'}), 404  # Devolver código 404 si el empleado no existe

    except ValidationError as err:
        return jsonify({'error': err.messages}), 400  # Devolver mensajes de error de validación con el código 400 (error de solicitud)

# Ruta para eliminar un empleado mediante una solicitud DELETE
@app.route('/empleados/<id>', methods=['DELETE'])
def delete_empleado(id):
    try:
        empleado = Empleado.query.get(id)

        # Verificar si el empleado existe en la base de datos
        if empleado:
            db.session.delete(empleado)
            db.session.commit()
            return empleado_schema.jsonify(empleado)
        else:
            return jsonify({'error': 'Empleado no encontrado'}), 404  # Devolver código 404 si el empleado no existe

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Devolver código 500 si hay un error durante la eliminación


if __name__ == '__main__':
    app.run(debug=True)

