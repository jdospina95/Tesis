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
administradores = db.administradores
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
    
def generarActividad1(numNumeroAntes, numNumeroDespues, numNumeroEntre, numValorPosicional, numResta, numSuma, numMultiplicacion, minn, maxn):
    preguntas = []
    
    acciones = json.load(open('database/acciones.json'))
    comidas = json.load(open('database/comidas.json'))
    personas = json.load(open('database/personas.json'))
    objetos = json.load(open('database/objetos.json'))
    
    for i in range(numNumeroAntes):
        preguntas.append(numeroAntes(minn,maxn))
        
    for i in range(numNumeroDespues):
        preguntas.append(numeroDespues(minn,maxn))
        
    for i in range(numNumeroEntre):
        preguntas.append(numeroEntre(minn,maxn))
        
    for i in range(numNumeroEntre):
        preguntas.append(numeroEntre(minn,maxn))
        
    for i in range(numValorPosicional):
        persona = personas[randint(0,len(personas)-1)]
        objeto = objetos[randint(0,len(objetos)-1)]
        preguntas.append(valorPosicional(persona, objeto, minn, maxn))
        
    for i in range(numResta):
        persona = personas[randint(0,len(personas)-1)]
        comida = comidas[randint(0,len(comidas)-1)]
        preguntas.append(resta(persona, comida, minn, maxn))

    for i in range(numSuma):
        persona1 = personas[randint(0,len(personas)-1)]
        persona2 = personas[randint(0,len(personas)-1)]
        
        while(persona1 == persona2):
            persona2 = personas[randint(0,len(personas)-1)]
        
        indiceAccion = acciones[randint(0,len(acciones)-1)]
        accion = indiceAccion['accion']
        accionPasado = indiceAccion['accionPasado']
        
        preguntas.append(suma(persona1, persona2, accion, accionPasado, minn, maxn))
    
    for i in range(numMultiplicacion):
        persona = personas[randint(0,len(personas)-1)]
        objeto = objetos[randint(0,len(objetos)-1)]
        preguntas.append(multiplicacion(persona, objeto, minn, maxn))
    
    return preguntas

def generarActividad2(numConjuntosIguales, numConjuntoMayor, numConjuntoMenor, numContarSonidos):
    preguntas = []
    
    animales = json.load(open('database/animales.json'))

    for i in range(numConjuntosIguales):
        animal1 = animales[randint(0,len(animales)-1)]
        animal2 = animales[randint(0,len(animales)-1)]
        while(animal1 == animal2):
            animal2 = animales[randint(0,len(animales)-1)]
            
        preguntas.append(conjuntosIguales(animal1,animal2))
        
    for i in range(numConjuntoMayor):
        animal1 = animales[randint(0,len(animales)-1)]
        animal2 = animales[randint(0,len(animales)-1)]
        while(animal1 == animal2):
            animal2 = animales[randint(0,len(animales)-1)]
            
        preguntas.append(conjuntoMayor(animal1,animal2))
    
    for i in range(numConjuntoMenor):
        animal1 = animales[randint(0,len(animales)-1)]
        animal2 = animales[randint(0,len(animales)-1)]
        while(animal1 == animal2):
            animal2 = animales[randint(0,len(animales)-1)]
            
        preguntas.append(conjuntoMenor(animal1,animal2))
        
    for i in range(numContarSonidos):
        animal1 = animales[randint(0,len(animales)-1)]
        animal2 = animales[randint(0,len(animales)-1)]
        while(animal1 == animal2):
            animal2 = animales[randint(0,len(animales)-1)]
            
        preguntas.append(contarSonidos(animal1,animal2))

    return preguntas

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', sesion = session)
    
@app.route('/GenerarReporte', methods=['GET'])
@login_required         #Validacion de inicio de sesion
def generarreporte():
    reg = []
    usuario = loads(session['usuario'])
    for respuesta in respuestas.find({'id_usuario': ObjectId(usuario['_id'])}):
        respuesta.pop('_id', None)
        respuesta.pop('id_usuario', None)
        reg.append(respuesta)
    return render_template('generarReporte.html', actividades=reg, usuario=(usuario['nombre'] + ' ' + usuario['apellido']))
    
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
        preguntas = generarActividad1(int(data['numeroAntes']), int(data['numeroDespues']), int(data['numeroEntre']), int(data['valorPosicional']), int(data['resta']), int(data['suma']), int(data['multiplicacion']), int(data['minn']), int(data['maxn']))
        
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
        return render_template('preguntas.html', preguntas=preguntasJavascript, respuestas=respuestasJavascript, numeros=numerosTexto, imagenes=imagenesJavascript, animales1 = [], animales2 = [], totalConjuntosA = [], totalConjuntosB = [],conf=config)
    else:
        return render_template('actividad1.html')
    
@app.route('/Actividad2', methods=['GET', 'POST'])
@login_required         #Validacion de inicio de sesion
def actividad2():
    if request.method == 'POST':
        fdata = request.form
        data = {}
        for (k,v) in fdata.items():
            data[k]=v
        preguntas = generarActividad2(int(data['conjuntosIguales']), int(data['conjuntoMayor']), int(data['conjuntoMenor']), int(data['contarSonidos']))
        
        preguntasJavascript, respuestasJavascript, imagenesJavascript, animales1Javascript, animales2Javascript, totalConjuntosAJavascript, totalConjuntosBJavascript = [], [], [], [], [], [], []
        for i in range(len(preguntas)):
            preguntasJavascript.append(str(preguntas[i][0]))
            respuestasJavascript.append(preguntas[i][1])
            imagenesJavascript.append(str(preguntas[i][2]))
            animales1Javascript.append(str(preguntas[i][3]))
            animales2Javascript.append(str(preguntas[i][4]))
            totalConjuntosAJavascript.append(str(preguntas[i][5]))
            totalConjuntosBJavascript.append(str(preguntas[i][6]))
            
        deserializedSession = loads(session['usuario'])
        deserializedSession['configuracion']
        conf = configuraciones.find_one({'_id': ObjectId(deserializedSession['configuracion'])})
        config = [str(conf['color_fondo']), str(conf['color_fuente']), str(conf['tamano_fuente'])+'px']
        numerosTexto = dumps(json.load(open('database/numeros.json')))
        
        return render_template('preguntas.html', preguntas=preguntasJavascript, respuestas=respuestasJavascript, numeros=numerosTexto, imagenes=imagenesJavascript, animales1 = animales1Javascript, animales2 = animales2Javascript, totalConjuntosA = totalConjuntosAJavascript, totalConjuntosB = totalConjuntosBJavascript, conf=config)
    else:
        return render_template('actividad2.html')
    
@app.route('/Actividad3', methods=['GET', 'POST'])
@login_required         #Validacion de inicio de sesion
def actividad3():
    if request.method == 'POST':
        fdata = request.form
        data = {}
        for (k,v) in fdata.items():
            data[k]=v
        preguntas = generarActividad1(int(data['numeroAntes']), int(data['numeroDespues']), int(data['numeroEntre']), int(data['minn']), int(data['maxn']))
        
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
    data['fecha'] = date.today().strftime("%-d de %B de %Y")
    data['hora'] = date.today().strftime("%-I:%M %p")
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
    
@app.route('/MenuAdministrador')
def menuAdministrador():
    global session
    return render_template('menuAdmin.html', sesion = session)
    
@app.route('/IniciarSesionAdministrador', methods=['GET', 'POST'])
def administrador():
    if request.method == 'POST':
        query = {"$and":[ {"usuario": str(request.form['usuario'])}, {"contrasena": str(request.form['contrasena'])}]}
        resultado = administradores.find(query)
        if resultado.count() > 0:
            return redirect('/MenuAdministrador')
        else:
            return render_template('iniciarSesionAdmin.html', error=True)
    else:
        return render_template('iniciarSesionAdmin.html')
        
@app.route('/AgregarObjeto', methods=['GET', 'POST'])
def agregarObjeto():
    if request.method == 'POST':
        return render_template('agregarObjeto.html')
    else:
        return render_template('agregarObjeto.html')

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