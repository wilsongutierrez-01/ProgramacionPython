
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
from flask import Flask, redirect, render_template, request, flash, url_for
import extras
import aiPredict
import mongoDB

db = 'visionDB'

app = Flask(__name__)
app.secret_key = 'darkCode'

# Mostrar pagina principal
@app.route('/')
def index():
    return render_template('pages/login.html')

@app.route('/inicio')
def inicio():
    return render_template('pages/index.html')

#Para abrir el formulario de crear una nueva cuenta
@app.route('/crearCuenta')
def crearCuenta():
    return render_template('pages/crearcuenta.html')

@app.route('/perfil')
def perfil():
    return render_template('pages/perfil.html')

@app.route('/predicciones')
def predicciones():
    return render_template('pages/predict.html')

#Para crear una nueva cuenta
@app.route('/crearUsuario', methods=['GET', 'POST'])
def crearUsuario():
    nombre = str(request.form['txtNombre'])
    apellido = str(request.form['txtApellido'])    
    correo = str(request.form['txtCorreo'])
    contra = str(request.form['txtContra'])
    contraConfir = str(request.form['txtConfirContra'])
    
    if extras.verificar_correo(correo) != True:
        flash('Correo invalido')
        return redirect(url_for('crearCuenta'))
    elif extras.verificar_contra(contra) != True:
        flash('Constraseña invalida')
        return redirect(url_for('crearCuenta'))
    elif contra != contraConfir:
        flash('Contraseñas no coinciden')
        return redirect(url_for('crearCuenta'))
    else:
        user = {'nombre':nombre, 'apellido':apellido, 'correo':correo, 'contra':contra}
        mongoDB.connection('visionDB','Usuarios')  
        mongoDB.save(user)
        flash('Usuario creado')
        return index()
    return None

@app.route('/about')
def about():
    return render_template('pages/about.html')
#Para iniciar sesion
@app.route('/iniciarSesion', methods=['GET', 'POST'])
def iniciarSesion():
    correo = request.form['txtCorreo']
    contra = request.form['txtContra']
    mongoDB.connection('visionDB','Usuarios')
    #Obtenemos los datos de contra
    contraDB = mongoDB.showUser('correo',correo)
    #Obtenemos los datos de correo
    correoDB = mongoDB.showUser('correo', correo)
    
    if contraDB != None and contraDB != None:    
        contrauser = contraDB['contra']
        correouser = correoDB['correo']
        if contra != contrauser or correo != correouser:
            flash('Contraseña incorrecta')
            return index()
        else:
            return inicio()
    else:
        flash('el usuario no existe')
        return index()
    
    pass
@app.route('/guardarData', methods=['GET', 'POST'])
def guardarData():
    global sim1, sim2, apertura, cierre
    sim1 = str(request.form['txtSimbolo1'])
    sim2 = str(request.form['txtSimbolo2'])
    apertura = str(request.form['txtFechaApertura'])
    cierre = str(request.form['txtFechaCierre'])
    prediccion = aiPredict.predecir(sim1,sim2,apertura,cierre,50)
    
    return render_template('pages/predict.html', Petroleo=prediccion, sim1=sim1, sim2=sim2)

#Con este metodo hacemos las predicciones
@app.route('/predecir')
def predecir():
    pass
# Mostrar simbolos
@app.route('/simbolos')
def simbolos():
    mongoDB.connection(db,'divisas')
    divisaSimboloDB = mongoDB.show('Símbolo')
    divisasNombresDB = mongoDB.show('Nombre')
    
    mongoDB.connection(db,'futuros')
    futuroSimboloDB = mongoDB.show('Símbolo')
    futuroNombreDB = mongoDB.show('Nombre')
    
    mongoDB.connection(db,'indices')
    indiceSimboloDB = mongoDB.show('Símbolo')
    indiceNombreDB = mongoDB.show('Nombre')   
    
    return render_template('pages/simbolos.html', divisaNombres=divisasNombresDB, len = len(divisaSimboloDB), divisaSimbolos=divisaSimboloDB,
                           futuroNombres=futuroNombreDB, lenfuturo = len(futuroNombreDB), futuroSimbolos=futuroSimboloDB,
                           indiceNombres=indiceNombreDB, lenindice = len(indiceNombreDB), indiceSimbolos=indiceSimboloDB)

if __name__ == '__main__':
    app.run(debug=True)