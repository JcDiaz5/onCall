from flask import render_template,request, redirect, flash, session
from flask_app.models.especialista import Especialista
from flask_app.models.clinica import Clinica
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# REGISTRAR ESPECIALISTA...........................
@app.route('/crear_especialista')
def crear_especialista():
    return render_template('registro_especialista.html')

@app.route('/registrar_especialista', methods=['POST'])
def registrar_especialista():
    if not Especialista.validate_especialista(request.form):
        return redirect("/crear_especialista")
    email = { "email" : request.form["email"] }
    especialista_en_bd = Especialista.get_by_email(email)
    if especialista_en_bd:
        flash("Una cuenta que utiliza ese correo ya ha sido registrada. Favor de elegír un correo distinto.")
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['contraseña'])
    data = {
        "nombre": request.form['nombre'],
        "email": request.form['email'],
        "contraseña" : pw_hash
    }
    especialista_id = Especialista.guardar(data)
    session['especialista_id'] = especialista_id
    return redirect("/especialista_dash")