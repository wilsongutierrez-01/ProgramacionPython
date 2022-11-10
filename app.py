
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
from flask import Flask, redirect, render_template, request

import aiPredict
import mongoDB

db = 'visionDB'

app = Flask(__name__)

# Mostrar pagina principal
@app.route('/')
def index():
    return render_template('pages/index.html')

@app.route('/inicio')
def inicio():
    return redirect('/')


@app.route('/guardarData', methods=['GET', 'POST'])
def guardarData():
    sim1 = str(request.form['txtSimbolo1'])
    sim2 = str(request.form['txtSimbolo2'])
    apertura = str(request.form['txtFechaApertura'])
    cierre = str(request.form['txtFechaCierre'])
    
    prediccion = aiPredict.predecir(sim1,sim2,apertura,cierre,50)
    return render_template('pages/predict.html', Petroleo=prediccion)

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