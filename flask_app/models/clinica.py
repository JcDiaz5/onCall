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
    def save(cls, data):
        query="""
        INSERT INTO clinicas(nombre, dueño, email, telefono, ubicacion, contraseña) 
        VALUES (%(nombre)s, %(dueño)s, %(email)s, %(telefono)s, %(ubicacion)s, %(contraseña)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM clinicas WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_one(cls, clinica_id):
        query  = "SELECT * FROM clinicas WHERE id = %(id)s;"
        data = {'id': clinica_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if not results:
            return None
        return cls(results[0])

# Validations............
    @staticmethod
    def validate_clinica(clinica):
        is_valid = True
        if len(clinica["nombre"]) < 2:
            flash("Nombre debe contener al menos 2 letras.")
            is_valid = False
        if len(clinica["dueño"]) < 2:
            flash("Nombre del dueño debe contener al menos 2 letras.")
            is_valid = False
        if not EMAIL_REGEX.match(clinica['email']):
            flash("Email invalido.")
            is_valid = False
        if len(clinica["telefono"]) < 10:
            flash("Teléfono debe de contener al menos 10 digitos.")
            is_valid = False
        if len(clinica["ubicacion"]) < 8:
            flash("Ubicación debe contener al menos 8 caracteres.")
            is_valid = False
        if len(clinica["contraseña"]) < 8:
            flash("Contraseña debe contener al menos 8 caracteres.")
            is_valid = False
        if (clinica["conf_contraseña"]) != (clinica["contraseña"]):
            flash("Contraseñas no coinciden.")
            is_valid = False
        return is_valid