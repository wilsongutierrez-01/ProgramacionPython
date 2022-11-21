from flask import jsonify
from matplotlib.font_manager import json_load
from pymongo import MongoClient
import json

from requests import PreparedRequest

def connection (dbs,collection_name):
    
    global client 
    global db
    global collection 
    
    client = MongoClient('mongodb://localhost')
    db = client[dbs]
    collection = db[collection_name]
    
    

def save(product):
    collection.insert_one(product)
    
    
def delete():
    collection.delete_many({})\

def show(nombreValor):
    data = collection.find({})
    datos = []
    cursor = data
    for i in cursor:
        datos.append(i[nombreValor])
    return datos

def showUser(value,val):
    data = collection.find_one({value:val})
    return data

def showby2(value,val):
    data = collection.find({value:val})
    return data

def getData():
    data = collection.find()
    name = collection.find({},{"name":1,"_id":0})
    cantidad = collection.find({},{"cantidad":1,"_id":0})
    precio = collection.find_one({},{"precio":1,"_id":0})
    # data = [name,cantidad,precio]
    return data

def arrayDatos(nombreValor, cursorDatos):
    datos = []
    cursor = cursorDatos
    for i in cursor:
        datos.append(i[nombreValor])
    
    return datos

def updateOne(value, val):
    collection.update_one(value,val)