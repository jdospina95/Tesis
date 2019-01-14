@app.route('/Actividad1', methods=['GET', 'POST'])
# @login_required         #Validacion de inicio de sesion
def actividad1():
    if request.method == 'POST':
        # deserializedSession = loads(session['usuario'])
        # query = { "_id": ObjectId(deserializedSession['_id'])}
        # deserializedSession['configuracion'] = request.form['id_configuracion']
        # nuevaConfiguracion = { "$set": { "configuracion": request.form['id_configuracion'] } }
        # usuarios.update_one(query, nuevaConfiguracion)
        # session['usuario'] = dumps(deserializedSession)
        fdata = request.form
        data = {}
        for (k,v) in fdata.items():
            data[k]=v
        preguntas = generarActividad1(int(data['operacionesbasicasA']), int(data['operacionesbasicasB']), int(data['minn']), int(data['maxn']))
        return render_template('preguntas.html', preguntas=preguntas, conf=configuracion)
    else:
        return render_template('actividad1.html')