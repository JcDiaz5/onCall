from flask import render_template,request, redirect, flash, session
from flask_app.models.clinica import Clinica
from flask_app.models.especialista import Especialista
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

# LOGIN CLINICA ......................................
@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    clinica_in_db = Clinica.get_by_email(data)
    especialista_in_db = Especialista.get_by_email(data)
    if clinica_in_db and bcrypt.check_password_hash(clinica_in_db.contraseña, request.form['contraseña']):
        session['clinica_id'] = clinica_in_db.id
        return redirect("/clinica_dash")
    elif especialista_in_db and bcrypt.check_password_hash(especialista_in_db.contraseña, request.form['contraseña']):
        session['especialista_id'] = especialista_in_db.id
        return redirect("/especialista_dash")
    flash("Email/Contraseña Invalido.")
    return redirect("/")

@app.route('/clinica_dash')
def clinica_dashboard():
    if 'clinica_id' not in session:
        return redirect('/')
    clinica=Clinica.get_one(session['clinica_id'])
    return render_template('clinica_dash.html', clinica=clinica)

@app.route('/lista_especialistas')
def lista_especialistas():
    especialistas = Especialista.get_all(id)
    return render_template('especialista_lista.html', especialistas=especialistas)

# LOGUT CLINICA ........................................
@app.route('/clinica_logout')
def clinica_logout():
    session.clear()
    return redirect('/')