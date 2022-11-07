
from flask import Flask, render_template, request, redirect
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas_datareader as pds
import pandas as pd
import seaborn as sb
import numpy as np

#//////////////////////////////////////////////////////////////
#Pruebas con inteligencia artificial para valores de la bolsa
#/////////////////////////////////////////////////////////////

# #Cargamos datos
# Petroleo = pds.DataReader("CL=F", "yahoo", start='2020-05-10', end='2022-05-10')
# Oro = pds.DataReader("GC=F", "yahoo", start='2020-05-10', end='2022-05-10')

# #vizualizamos datos
# print("Petroleo: ",Petroleo.Close, "Oro: ",Oro.Close)

# #Capa para conectar los datos de entrada con los de salida
# capa = tf.keras.layers.Dense(units = 1, input_shape=[1])

# #Creamos modelo secuencial para este caso
# #Usamos funcion de perdida de error cuadratico medio
# #Usamo optimizador de Adamax para mejorar modelo conforme se entrena

# modelo = tf.keras.Sequential([capa])
# modelo.compile(
#     optimizer = tf.keras.optimizers.Adamax(0.1),
#     loss = "mean_squared_error"
# )

# #Entrenamos el modelo. Le decimos a la funcion fit que lo haga 100 veces con epoch
# #Mucho o poco? se sabra al graficar
# historico = modelo.fit(Petroleo.Close, Oro.Close, epochs = 100, verbose = False)

# p = modelo.predict([50])
# p = p[0][0]

#//////////////////////////////////////////////////////////////


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
    
    Petroleo = pds.DataReader(sim1, "yahoo", start=apertura, end=cierre)
    Oro = pds.DataReader(sim2,"yahoo", start=apertura, end=cierre)
    #Capa para conectar los datos de entrada con los de salida
    capa = tf.keras.layers.Dense(units = 1, input_shape=[1])

    #Creamos modelo secuencial para este caso
    #Usamos funcion de perdida de error cuadratico medio
    #Usamo optimizador de Adamax para mejorar modelo conforme se entrena

    modelo = tf.keras.Sequential([capa])
    modelo.compile(
        optimizer = tf.keras.optimizers.Adamax(0.1),
        loss = "mean_squared_error"
    )

    #Entrenamos el modelo. Le decimos a la funcion fit que lo haga 100 veces con epoch
    #Mucho o poco? se sabra al graficar
    historico = modelo.fit(Petroleo.Close, Oro.Close, epochs = 100, verbose = False)


    pr = modelo.predict([50])
    pr = pr[0][0]
    return render_template('pages/predict.html', Petroleo=pr)

# Mostrar simbolos
@app.route('/simbolos')
def simbolos():
    return render_template('pages/simbolos.html')

if __name__ == '__main__':
    app.run(debug=True)