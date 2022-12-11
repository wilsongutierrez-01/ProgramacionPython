import tensorflow as tf
import pandas_datareader as pds

#Nuestras varibales globales para poder llamar desde cualaquier parte de nuestra AI
simboloComparacion = ''
simboloPredecir = ''

# con esto tomamos los datos desde el formulario 
def datos(sim1,sim2,apertura,cierre):
    global simboloComparacion,simboloPredecir
    simboloComparacion = pds.DataReader(sim1, "yahoo", start=apertura, end=cierre)
    simboloPredecir = pds.DataReader(sim2,"yahoo", start=apertura, end=cierre)
    
    pass


# datos('CL=F','GC=F','01-01-2020','01-01-2022')
# print(simboloComparacion)
#Tomamos cada varible de manera individual

# def comparacion(sim1,apertura,cierre):
#     simboloComparacion = pds.DataReader(sim1, "yahoo", start=apertura, end=cierre)
#     return simboloComparacion

# def prediciendo(sim2,apertura,cierre):
#     simboloPredecir = pds.DataReader(sim2,"yahoo", start=apertura, end=cierre)
#     return simboloPredecir

#Guardamos los valores dentro de variables en nuestra AI

def predecir(valor):
    # simboloComparacion = pds.DataReader(sim1, "yahoo", start=apertura, end=cierre)
    # simboloPredecir = pds.DataReader(sim2,"yahoo", start=apertura, end=cierre)
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
    historico = modelo.fit(simboloComparacion.Close, simboloPredecir.Close, epochs = 100, verbose = False)
    prediccion = modelo.predict([valor])
    prediccion = prediccion[0][0]
    
    return prediccion