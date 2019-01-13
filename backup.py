import os,sys
import subprocess
from flask import Flask, render_template, request, redirect, jsonify, session
import json
from pymongo import MongoClient     #Pymongo Framework -> MongoDB

app = Flask(__name__)

session = ''

client = MongoClient('mongodb://usuario:123456789a@ds031835.mlab.com:31835/tesis')        #Conexion con MongoDB en MongoLab
db = client['tesis']
usuarios = db.usuarios                                                                    #Referencia a la coleccion "Usuarios" de la DB
configuraciones = db.configuraciones                                                      #Referencia a la coleccion "Configuraciones" de la DB
personas = db.personas                                                                    #Referencia a la coleccion "Usuarios" de la DB
comidas = db.comidas                                                                      #Referencia a la coleccion "Configuraciones" de la DB
cosas = db.cosas                                                                          #Referencia a la coleccion "Usuarios" de la DB

@app.route('/', methods=['GET'])
def index():
    global session
    return render_template('index.html', sesion = session)
    
@app.route('/IniciarSesion', methods=['GET', 'POST'])
def iniciarsesion():
    global session
    if request.method == 'POST':
        session = request.form['nom_usuario']
        return redirect('/MenuInicio')
    else:
        reg = []
        for usuario in usuarios.find():         #Query .find() = SELECT *
            data = usuario
            reg.append({'nombre':data['nombre'], 'apellido':data['apellido']})
        return render_template('iniciarSesion.html', usuarios=reg)

@app.route('/RegistrarUsuario', methods=['GET', 'POST'])
def registrarusuario():
    #usuarios.delete_many({})        #Borra todos los registros de la coleccion usuarios
    if request.method == 'POST':
        fdata = request.form
        data = {}
        for (k,v) in fdata.items():
            data[k]=v
        usuarios.insert_one(data)       #Inserta un solo registro a la coleccion "Usuarios"
        return redirect('/')
    else:
        return render_template('registrarUsuario.html')

@app.route('/MenuInicio')    
def menuInicio():
    global session
    return render_template('menuInicio.html', sesion = session)

@app.route('/Configuracion', methods=['GET', 'POST'])
def configuracion():
    global session
    if request.method == 'POST':
        #session = request.form['nom_usuario']
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
            reg.append({'nombre':data['nombre'], 'tamano_fuente':data['tamano_fuente'], 'color_fuente':data['color_fuente'], 'color_fondo':data['color_fondo']})
        return render_template('configuracion.html',configuraciones=reg)

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))