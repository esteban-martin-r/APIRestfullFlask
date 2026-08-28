from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, fields, marshal_with
from models import db, Juego 

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

juego_fields = {
    'id': fields.Integer,
    'nombre': fields.String,
    'descripcion': fields.String,
    'precio': fields.Float
}

class JuegoList(Resource):
    @marshal_with(juego_fields)
    def get(self):
        juegos = Juego.query.all()
        return juegos, 200

    def post(self):
        data = request.get_json()
        if not data or not all(k in data for k in ('nombre', 'descripcion', 'precio')):
            return {'error': 'Faltan datos obligatorios'}, 400
        
        nuevo_juego = Juego(
            nombre=data['nombre'],
            descripcion=data['descripcion'],
            precio=float(data['precio'])
        )
        db.session.add(nuevo_juego)
        db.session.commit()
        return {'mensaje': 'Juego creado correctamente'}, 201

class JuegoResource(Resource):
    @marshal_with(juego_fields)
    def get(self, id):
        juego = Juego.query.get(id)
        if not juego:
            return {'error': 'Juego no encontrado'}, 404
        return juego, 200

    def put(self, id):
        data = request.get_json()
        juego = Juego.query.get(id)
        if not juego:
            return {'error': 'Juego no encontrado'}, 404
        
        if 'nombre' in data: juego.nombre = data['nombre']
        if 'descripcion' in data: juego.descripcion = data['descripcion']
        if 'precio' in data: juego.precio = float(data['precio'])
        
        db.session.commit()
        return {'mensaje': 'Juego actualizado correctamente'}, 200

    def delete(self, id):
        juego = Juego.query.get(id)
        if not juego:
            return {'error': 'Juego no encontrado'}, 404
        db.session.delete(juego)
        db.session.commit()
        return '', 204

api.add_resource(JuegoList, '/api/juegos')
api.add_resource(JuegoResource, '/api/juegos/<int:id>')
