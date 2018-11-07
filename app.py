import os,sys
import subprocess
from flask import Flask, render_template, request, redirect, jsonify
import json
app = Flask(__name__)

session = ''

@app.route('/', methods=['GET'])
def index():
    global session
    return render_template('index.html', sesion = session)
    
@app.route('/IniciarSesion', methods=['GET', 'POST'])
def iniciarsesion():
    global session
    if request.method == 'POST':
        session = request.form['nom_usuario']
        return redirect('/')
    else:
        files = os.listdir('database')
        reg = []
        for fname in files:
            with open("database/"+fname,"r") as f:
                data = json.load(f)
                reg.append({'nombre':data['nombre'], 'apellido':data['apellido']})
        return render_template('iniciarSesion.html',usuarios=reg)
    
@app.route('/RegistrarUsuario', methods=['GET', 'POST'])
def registrarusuario():
    if request.method == 'POST':
        fdata = request.form
        data = {}
        for (k,v) in fdata.items():
            data[k]=v
        nombre,apellido = data['nombre'],data['apellido']
        with open("database/"+nombre+apellido+".json","w") as f:
            json.dump(data,f)
        return redirect('/')
    else:
        return render_template('registrarUsuario.html')

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))