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
import locale
from datetime import date
#https://rawgit.com/MrRio/jsPDF/master/

app = Flask(__name__)
app.secret_key = os.urandom(24)     #LLave para envio de session

client = MongoClient('mongodb://usuario:123456789a@ds031835.mlab.com:31835/tesis')        #Conexion con MongoDB en MongoLab
db = client['tesis']
usuarios = db.usuarios                                                                    #Referencia a la coleccion "Usuarios" de la DB
configuraciones = db.configuraciones                                                      #Referencia a la coleccion "Usuarios" de la DB
respuestas = db.respuestas

locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

def login_required(f):
    @wraps(f)
    def wrap():
        if 'usuario' not in session:
            return redirect('/IniciarSesion')
        else:
            return f()
    return wrap           #Nueva funcion para validacion de sesion iniciada
    
def generarActividad1(basicasA, basicasB, minn, maxn):
    preguntas = []
    
    acciones = json.load(open('database/acciones.json'))
    comidas = json.load(open('database/comidas.json'))
    personas = json.load(open('database/personas.json'))
    
    for i in range(basicasA):
        persona = personas[randint(0,len(personas)-1)]
        comida = comidas[randint(0,len(comidas)-1)]
        
        preguntas.append(OperacionesBasicasA(persona,comida,minn,maxn))
        
    for i in range(basicasB):
        persona1 = personas[randint(0,len(personas)-1)]
        persona2 = personas[randint(0,len(personas)-1)]
        accion = acciones[randint(0,len(acciones)-1)]
        accionpasado = accion["accionpasado"]
        accion = accion["accion"]
        
        preguntas.append(OperacionesBasicasB(persona1,persona2,accion,accionpasado,minn,maxn))
    
    return preguntas

@app.route('/', methods=['GET'])
def index():
    global session
    return render_template('index.html', sesion = session)
    
@app.route('/GenerarReporte', methods=['GET'])
@login_required         #Validacion de inicio de sesion
def generarreporte():
    reg = []
    deserializedSession = loads(session['usuario'])
    for respuesta in respuestas.find({'id_usuario': ObjectId(deserializedSession['_id'])}):
        respuesta.pop('_id', None)
        respuesta.pop('id_usuario', None)
        reg.append(respuesta)
    return render_template('generarReporte.html', actividades=reg)
    
@app.route('/SeleccionarActividad', methods=['GET'])
@login_required         #Validacion de inicio de sesion
def seleccionaractividad():
    return render_template('seleccionarActividad.html')
    
@app.route('/Actividad1', methods=['GET', 'POST'])
@login_required         #Validacion de inicio de sesion
def actividad1():
    if request.method == 'POST':
        
        fdata = request.form
        data = {}
        for (k,v) in fdata.items():
            data[k]=v
        preguntas = generarActividad1(int(data['operacionesbasicasA']), int(data['operacionesbasicasB']), int(data['minn']), int(data['maxn']))
        
        preguntasJavascript, respuestasJavascript, imagenesJavascript = [],[],[]
        for i in range(len(preguntas)):
            preguntasJavascript.append(str(preguntas[i][0]))
            respuestasJavascript.append(preguntas[i][1])
            imagenesJavascript.append(str(preguntas[i][2]))
        
        deserializedSession = loads(session['usuario'])
        deserializedSession['configuracion']
        conf = configuraciones.find_one({'_id': ObjectId(deserializedSession['configuracion'])})
        config = [str(conf['color_fondo']), str(conf['color_fuente']), str(conf['tamano_fuente'])+'px']
        numerosTexto = dumps(json.load(open('database/numeros.json')))
        return render_template('preguntas.html', preguntas=preguntasJavascript, respuestas=respuestasJavascript, numeros=numerosTexto, imagenes=imagenesJavascript, conf=config)
    else:
        return render_template('actividad1.html')
    
@app.route('/Actividad2', methods=['GET', 'POST'])
@login_required         #Validacion de inicio de sesion
def actividad2():
    return render_template('actividad2.html')
    
@app.route('/Actividad3', methods=['GET', 'POST'])
@login_required         #Validacion de inicio de sesion
def actividad3():
    return render_template('actividad3.html')
    
@app.route('/GuardarResultados', methods=['POST'])
@login_required         #Validacion de inicio de sesion
def guardarResultados():
    fdata = request.form
    data = {}
    for (k,v) in fdata.items():
        data[k]=v
        
    deserializedSession = loads(session['usuario'])
    data['id_usuario'] = ObjectId(deserializedSession['_id'])
    # sudo locale-gen es_ES.UTF-8 
    data['fecha'] = date.today().strftime("%d de %B de %Y")
    respuestas.insert_one(data)
    return redirect('/MenuInicio')
    
@app.route('/VerificarProgreso', methods=['GET', 'POST'])
@login_required         #Validacion de inicio de sesion
def verificarprogreso():
    return render_template('verificarProgreso.html')

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

@app.route('/CerrarSesion', methods=['GET'])
@login_required         #Validacion de inicio de sesion
def cerrarSesion():
    session.clear()
    return render_template('index.html', sesion = session)

@app.route('/RegistrarUsuario', methods=['GET', 'POST'])
def registrarusuario():
    #usuarios.delete_many({})        #Borra todos los registros de la coleccion usuarios
    if request.method == 'POST':
        fdata = request.form
        data = {}
        for (k,v) in fdata.items():
            data[k]=v
            
        if configuraciones.find().count() == 0:
            configuraciones.insert_one({"nombre": "Default", "tamano_fuente": "76", "color_fuente": "white", "color_fondo": "black"})
        
        data['configuracion'] = ObjectId(configuraciones.find({"nombre":"Default"})[0]['_id'])#'default'           #se agrega comfiguracion default al registrar usuario
        usuarios.insert_one(data)       #Inserta un solo registro a la coleccion "Usuarios"
        return redirect('/')
    else:
        return render_template('registrarUsuario.html')

@app.route('/MenuInicio')    
@login_required         #Validacion de inicio de sesion
def menuInicio():
    global session
    return render_template('menuInicio.html', sesion = session)

@app.route('/Configuracion', methods=['GET', 'POST'])
@login_required         #Validacion de inicio de sesion
def configuracion():
    if request.method == 'POST':
        deserializedSession = loads(session['usuario'])
        query = { "_id": ObjectId(deserializedSession['_id'])}
        deserializedSession['configuracion'] = request.form['id_configuracion']
        nuevaConfiguracion = { "$set": { "configuracion": ObjectId(request.form['id_configuracion']) } }
        usuarios.update_one(query, nuevaConfiguracion)
        session['usuario'] = dumps(deserializedSession)
        return redirect('/MenuInicio')
    else:
        reg = []
        for configuracion in configuraciones.find():         #Query .find() = SELECT *
            data = configuracion
            reg.append({'_id':data['_id'],'nombre':data['nombre'], 'tamano_fuente':data['tamano_fuente'], 'color_fuente':data['color_fuente'], 'color_fondo':data['color_fondo']})
        return render_template('configuracion.html',configuraciones=reg)

@app.route('/EliminarUsuario', methods=['GET', 'POST'])
def eliminarUsuario():
    if request.method == 'POST':
        query = {"_id": ObjectId(request.form['nom_usuario'])}
        usuarios.delete_one(query)
        return redirect('/')
    else:
        reg = []
        for usuario in usuarios.find():         #Query .find() = SELECT *
            data = usuario
            reg.append({'_id':data['_id'], 'nombre':data['nombre'], 'apellido':data['apellido']})       #Se agraga campo _id para consultar usuario iniciado
        return render_template('eliminarUsuario.html',usuarios=reg)

@app.route('/NuevaConfiguracion', methods=['GET', 'POST'])
@login_required         #Validacion de inicio de sesion
def nuevaConfiguracion():
    if request.method == 'POST':
        fdata = request.form
        data = {}
        for (k,v) in fdata.items():
            data[k]=v
        configuraciones.insert_one(data)
        return redirect('/Configuracion')
    else:
        return render_template('nuevaConfiguracion.html')

@app.route('/EliminarConfiguracion', methods=['GET', 'POST'])
@login_required         #Validacion de inicio de sesion
def eliminarConfiguracion():
    if request.method == 'POST':
        query = {"_id": ObjectId(request.form['nom_configuracion'])}
        configuraciones.delete_one(query)
        return redirect('/Configuracion')
    else:
        reg = []
        for configuracion in configuraciones.find():         #Query .find() = SELECT *
            data = configuracion
            reg.append({'_id':data['_id'],'nombre':data['nombre'], 'tamano_fuente':data['tamano_fuente'], 'color_fuente':data['color_fuente'], 'color_fondo':data['color_fondo']})
        return render_template('eliminarConfiguracion.html',configuraciones=reg)

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))