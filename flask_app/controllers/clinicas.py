from flask import render_template,request, redirect, flash, session
from flask_app.models.clinica import Clinica
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    # if "clinica_id" in session:
    #     return redirect('/clinica_dash')
    # if "especialista_id" in session:
    #     return redirect('/especialista_dash')
    # else:
    return render_template('index.html')


# CREATE CLINICA...........................
@app.route('/registrar_clinica', methods=['POST'])
def registrar_clinica():
    if not Clinica.validate_clinica(request.form):
        return redirect("/")
    email = { "email" : request.form["email"] }
    clinica_en_bd = Clinica.get_by_email(email)
    if clinica_en_bd:
        flash("Una cuenta que utiliza ese correo ya ha sido registrada. Favor de elegír un correo distinto.")
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['contraseña'])
    data = {
        "nombre": request.form['nombre'],
        "dueño": request.form['dueño'],
        "email": request.form['email'],
        "telefono": request.form['telefono'],
        "ubicacion": request.form['ubicacion'],
        "contraseña" : pw_hash
    }
    clinica_id = Clinica.guardar(data)
    session['clinica_id'] = clinica_id
    return redirect("/clinica_dash")


