from flask import render_template,request, redirect, flash, session
from flask_app.models.especialista import Especialista
from flask_app.models.clinica import Clinica
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# REGISTRAR ESPECIALISTA...........................
@app.route('/registrar_especialista', methods=['POST'])
def registrar_especialista():
    if not Especialista.validate_especialista(request.form):
        return redirect("/")
    email = { "email" : request.form["email"] }
    if especialista_en_bd := Especialista.get_by_email(email):
        flash("Una cuenta que utiliza ese correo ya ha sido registrada. Favor de elegír un correo distinto.")
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['contraseña'])
    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "genero": request.form['genero'],
        "email": request.form['email'],
        "num_contacto": request.form['num_contacto'],
        "cedula": request.form['cedula'],
        "contraseña" : pw_hash
    }
    especialista_id = Especialista.save(data)
    session['especialista_id'] = especialista_id
    return redirect("/especialista_dash")

@app.route('/especialista_dash')
def dashboard_especialista():
    if 'especialista_id' not in session:
        return redirect('/')
    return render_template('especialista_dash.html')

@app.route('/especialista_logout')
def especialista_logout():
    session.clear()
    return redirect('/')
