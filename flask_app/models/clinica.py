import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models import clinica
from flask_app.models import especialista
from flask_app.config.mysqlconnection import connectToMySQL


class Clinica:
    DB ="onCall"
    def __init__(self,data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.dueño=data['dueño']
        self.email=data['email']
        self.telefono=data['telefono']
        self.ubicacion=data['ubicacion']
        self.contraseña=data['contraseña']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.confirm_contra=None

# CREATE CHEF..................
    @classmethod
    def guardar(cls, data):
        query="""
        INSERT INTO clinicas(nombre, dueño, email, telefono, ubicacion, contraseña) 
        VALUES (%(nombre)s, %(dueño)s, %(email)s, %(telefono)s, %(ubicacion)s, %(contraseña)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)