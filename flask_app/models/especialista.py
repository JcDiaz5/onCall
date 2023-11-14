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
        self.genero=data['genero']
        self.email=data['email']
        self.num_contacto=data['num_contacto']
        self.cedula=data['cedula']
        self.contraseña=data['contraseña']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.confirm_contra=None

# CREATE USER..................
    @classmethod
    def save(cls, data):
        query="""
        INSERT INTO especialistas(nombre, apellido, genero, email, num_contacto, cedula, contraseña) 
        VALUES (%(nombre)s, %(apellido)s,  %(genero)s, %(email)s, %(num_contacto)s, %(cedula)s, %(contraseña)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM especialistas WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM especialistas;"
        result = connectToMySQL(cls.DB).query_db(query)
        if len(result) < 1:
            return False
        return result
    
    @classmethod
    def get_one(cls, especialista_id):
        query  = "SELECT * FROM especialistas WHERE id = %(id)s;"
        data = {'id': especialista_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if not results:
            return None
        return cls(results[0])
    
    # Validations............................
    @staticmethod
    def validate_especialista(especialista):
        is_valid = True
        if len(especialista["nombre"]) < 2:
            flash("Nombre debe contener al menos 2 letras.")
            is_valid = False
        if len(especialista["apellido"]) < 2:
            flash("Apellidos debe contener al menos 2 letras.")
            is_valid = False
        if not EMAIL_REGEX.match(especialista['email']):
            flash("Email invalido.")
            is_valid = False
        if len(especialista["num_contacto"]) < 10:
            flash("Contacto debe de contener al menos 10 digitos.")
            is_valid = False
        if len(especialista["cedula"]) < 3:
            flash("Cédula Profesional debe contener al menos #### digitos.")
            is_valid = False
        if len(especialista["contraseña"]) < 8:
            flash("Contraseña debe contener al menos 8 caracteres.")
            is_valid = False
        if (especialista["conf_contraseña"]) != (especialista["contraseña"]):
            flash("Contraseñas no coinciden.")
            is_valid = False
        return is_valid