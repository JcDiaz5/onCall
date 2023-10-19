import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import clinica


class Especialista:
    DB = "onCall"
    def __init__(self,data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido=data['apellido']
        self.email=data['email']
        self.num_contacto=data['num_contacto']
        self.matricula=data['matricula']
        self.contraseña=data['contraseña']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.confirm_contra=None

# CREATE USER..................
    @classmethod
    def guardar(cls, data):
        query="""
        INSERT INTO especialistas(nombre,apellido, email, num_contacto, matricula, contraseña) 
        VALUES (%(nombre)s, %(apellido)s, %(email)s, %(num_contacto)s, %(matricula)s, %(contraseña)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)