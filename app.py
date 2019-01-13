import os,sys
import subprocess
import json
from preguntas import *
from functools import wraps     #Se agrega wraps para validacion de iniciada sesion
from flask import Flask, render_template, request, redirect, jsonify, session
from bson.objectid import ObjectId      #Se agreaga para poder consultar por _id
from bson.json_util import dumps, loads  #serializacion de OjectId de mongo
from pymongo import MongoClient     #Pymongo Framework -> MongoDB
from random import randint

app = Flask(__name__)
app.secret_key = os.urandom(24)     #LLave para envio de session

client = MongoClient('mongodb://usuario:123456789a@ds031835.mlab.com:31835/tesis')        #Conexion con MongoDB en MongoLab
db = client['tesis']
usuarios = db.usuarios                                                                    #Referencia a la coleccion "Usuarios" de la DB
configuraciones = db.configuraciones                                                      #Referencia a la coleccion "Usuarios" de la DB

def login_required(f):
    @wraps(f)
    def wrap():
        if 'usuario' not in session:
            return redirect('/IniciarSesion')
        else:
            return f()
    return wrap           #Nueva funcion para validacion de sesion iniciada
    
def generarActividad(basicasA, basicasB, maxn):
    actividad = []
    
    acciones = json.load(open('database/acciones.json'))
    comidas = json.load(open('database/comidas.json'))
    personas = json.load(open('database/personas.json'))
    
    for i in range(basicasA):
        persona = personas[randint(0,len(personas)-1)]
        comida = comidas[randint(0,len(comidas)-1)]
        
        print OperacionesBasicasA(persona,comida,maxn)
        
    for i in range(basicasB):
        persona1 = personas[randint(0,len(personas)-1)]
        persona2 = personas[randint(0,len(personas)-1)]
        accion = acciones[randint(0,len(acciones)-1)]
        accionpasado = accion["accionpasado"]
        accion = accion["accion"]
        
        print OperacionesBasicasB(persona1,persona2,accion,accionpasado,maxn)
    
    return actividad

@app.route('/', methods=['GET'])
def index():
    global session
    return render_template('index.html', sesion = session)
    
@app.route('/IniciarSesion', methods=['GET', 'POST'])
def iniciarsesion():
    if request.method == 'POST':
        #Cambio a traer usuario de BD y guardar datos en sesion
        query = {"_id": ObjectId(request.form['nom_usuario'])}
        resultado = usuarios.find(query)[0]
        resultado = dumps(resultado)
        session['usuario'] = resultado
        #Cambio a traer usuario de BD y guardar datos en sesion
        return redirect('/MenuInicio')
    else:
        reg = []
        for usuario in usuarios.find():         #Query .find() = SELECT *
            data = usuario
            reg.append({'_id':data['_id'], 'nombre':data['nombre'], 'apellido':data['apellido']})       #Se agraga campo _id para consultar usuario iniciado
        return render_template('iniciarSesion.html',usuarios=reg)


@app.route('/RegistrarUsuario', methods=['GET', 'POST'])
def registrarusuario():
    #usuarios.delete_many({})        #Borra todos los registros de la coleccion usuarios
    if request.method == 'POST':
        fdata = request.form
        data = {}
        for (k,v) in fdata.items():
            data[k]=v
        data['configuracion'] = configuraciones.find({"nombre":"Default"})[0]['_id']#'default'           #se agrega comfiguracion default al registrar usuario
        usuarios.insert_one(data)       #Inserta un solo registro a la coleccion "Usuarios"
        return redirect('/')
    else:
        return render_template('registrarUsuario.html')

@app.route('/MenuInicio')    
@login_required         #Validacion de inicio de sesion
def menuInicio():
    global session
    return render_template('menuInicio.html', sesion = session)

#TODO: Falta darle update a la configuracion seleccionada
@app.route('/Configuracion', methods=['GET', 'POST'])
@login_required         #Validacion de inicio de sesion
def configuracion():
    if request.method == 'POST':
        deserializedSession = loads(session['usuario'])
        query = { "_id": ObjectId(deserializedSession['_id'])}
        deserializedSession['configuracion'] = request.form['id_configuracion']
        nuevaConfiguracion = { "$set": { "configuracion": request.form['id_configuracion'] } }
        usuarios.update_one(query, nuevaConfiguracion)
        session['usuario'] = dumps(deserializedSession)
        return redirect('/MenuInicio')
    else:
        
        #Insercion de Data Configuracion. Mientras se mira como se llena.
        #configuraciones.delete_many({})        #Borra todos los registros de la coleccion configuraciones
        #insert = [
        #    {"nombre": "Default", "tamano_fuente": "12", "color_fuente": "Negro", "color_fondo": "Verde"},
        #    {"nombre": "Ciegos", "tamano_fuente": "12", "color_fuente": "Negro", "color_fondo": "Rojo"},
        #    {"nombre": "Muy Ciegos", "tamano_fuente": "9", "color_fuente": "Blanco", "color_fondo": "Amarillo"}    
        #]
        #configuraciones.insert_many(insert)      #Inserta en la Coleccion una lista de configuraciones 
        #Insercion de Data Configuracion. Mientras se mira como se llena.
        
        reg = []
        for configuracion in configuraciones.find():         #Query .find() = SELECT *
            data = configuracion
            reg.append({'_id':data['_id'],'nombre':data['nombre'], 'tamano_fuente':data['tamano_fuente'], 'color_fuente':data['color_fuente'], 'color_fondo':data['color_fondo']})
        return render_template('configuracion.html',configuraciones=reg)

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))