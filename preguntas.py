from random import randint

# Preguntas operaciones basicas
def OperacionesBasicasA(persona, comida, minn, maxn):
    # Si <persona> tiene <numero> <comida> y se come <numero>, cuanta(s) <comida> le queda(n)?
    numero1 = randint(minn,maxn)
    numero2 = randint(1,numero1)
    respuesta = numero1-numero2
    imagen = "/static/svgs/" + comida + ".svg"
    pregunta = 'Si '+persona+' tiene '+str(numero1)+' '+comida
    
    if comida[len(comida)-1] == 'a': cuanto = 'cuantas' 
    else: cuanto = 'cuantos'
    
    if numero1 > 1: pregunta = pregunta+'s y se come '+str(numero2)+', '+cuanto+' '+comida+'s le quedan?'  
    else: pregunta = pregunta+' y se come '+str(numero2)+', '+cuanto+' '+comida+' le quedan?'

    return [pregunta,respuesta,imagen]
    
def OperacionesBasicasB(persona1, persona2, accion, accionpasado, minn, maxn):
    # <persona> <accion> <numero> veces, <persona2> <accion> <numero> veces <mas|menos> que <persona>, cuantas veces <accionpasado> <persona2>?
    imagen = "/static/svgs/" + accion + ".svg"
    numero1 = randint(minn,maxn)
    numero2 = randint(1,minn)
    masmenos = randint(0,1) #0 mas, 1 menos
    
    if numero2 == 1:
        veces = 'vez'
    else:
        veces = 'veces'
    
    if masmenos == 0:
        respuesta = numero1 + numero2
        pregunta = persona1 + ' ' + accion + ' ' + str(numero1) + ' veces, ' + persona2 + ' ' + accionpasado + ' ' + str(numero2) + ' ' + veces + ' mas que ' + persona1 + ', cuantas veces ' + accionpasado + ' ' + persona2 + '?' 
    else:
        respuesta = numero1 - numero2
        pregunta = persona1 + ' ' + accion + ' ' + str(numero1) + ' veces, ' + persona2 + ' ' + accionpasado + ' ' + str(numero2) + ' ' + veces + ' menos que ' + persona1 + ', cuantas veces ' + accionpasado + ' ' + persona2 + '?' 

    return [pregunta,respuesta,imagen]

#Preguntas posicion numerica
def posicionNumericaA(persona,  maxn):
    numero1 = randint(1,maxn)
    
    if randint(1, 2) == 1: antesDespues, respuesta = 'antes', numero1 - 1 
    else: antesDespues, respuesta = 'despues ', numero1 + 1
    
    pregunta = persona + ' tiene el turno ' + str(numero1) + ' para jugar con el balon, que turno tiene la persona ' + antesDespues + ' que ' + persona + '?'
    return [pregunta, respuesta]

def posicionNumericaB(persona1, persona2, persona3):
    numero = 0
    if randint(1, 2) == 1:  
        numero = randint(1,10)
        antesDespues, respuesta = numero + 2, numero + 1
    else: 
        numero = randint(3,12) 
        antesDespues, respuesta = numero - 2, numero - 1
    
    pregunta = 'Un tren que sale a cada hora, el cual ' + persona1 + ' lo toma a las ' + str(numero) + ' y ' + persona2 + ' toma el tren a las ' + str(antesDespues) + ' a que hora tomo el tren ' + persona3 + ' si salio entre ' + persona1 + ' y ' + persona2 +'?' 
    return [pregunta, respuesta]

#Preguntas conjuntos 
def conjuntosA(persona1, persona2, objeto, maxn):
    objeto1 = objeto2 = objeto
    numero1 = randint(1, maxn)
    numero2 = randint(1, maxn)
    while numero2 == numero1:
        numero2 = randint(1, maxn)
        
    operacion = randint(1, 2)
    
    if operacion == 1: 
        operacion = 'mas'
        if numero1 > numero2: respuesta = persona1
        else: respuesta = persona2
    else: 
        operacion = 'menos'
        if numero1 > numero2: respuesta = persona2
        else: respuesta = persona1
    
    if numero1 != 1:
        objeto1 = objeto + 's'
        
    if numero2 != 1:
        objeto2 = objeto + 's'
    
    pregunta = 'Si ' + persona1 + ' tiene ' + str(numero1) + ' ' + objeto1 + ' y ' + persona2 + ' tiene ' + str(numero2) + ' ' + objeto2 + ', quien tiene ' + operacion + ' ' + objeto + 's?' 
    return [pregunta, respuesta]

def conjuntosB(persona1, persona2, objeto, maxn):
    objeto1 = objeto2 = objeto
    numero1 = randint(1, maxn)
    numero2 = randint(1, maxn)
    igualDiferente = randint(1,2)
    if randint(1, 2) == 1:
        numero2 = numero1
        
    if numero1 != 1:
        objeto1 = objeto + 's'
        
    if numero2 != 1:
        objeto2 = objeto + 's'
    
    if igualDiferente == 1: 
        igualDiferente = 'igual'
        if numero1 == numero2: respuesta = 'Si'
        else: respuesta = 'No'
    else:
        igualDiferente = 'difetente'
        if numero1 == numero2: respuesta = 'No'
        else: respuesta = 'Si'
    
    pregunta = 'Si ' + persona1 +' tiene ' + str(numero1) + ' ' + objeto1 + ', y ' + persona2 + ' tiene ' + str(numero2) + ' ' + objeto2 + ', ambos tienen ' + igualDiferente + ' numero de ' + objeto + 's?'
    
    return [pregunta, respuesta]

#Preguntas valor posicional
def ValorPosicional(persona, objeto, maxn):
    numero = randint(1,maxn)
    
    tamanoNumero = len(str(numero))
    unidad = randint(1, tamanoNumero)
    if unidad < 2: valorPosicional, respuesta = 'Unidades' , int(str(numero)[tamanoNumero - 1])
    elif unidad < 3: valorPosicional, respuesta = 'Decenas', int(str(numero)[tamanoNumero - 2] + '0')
    elif unidad < 4: valorPosicional, respuesta = 'Centenas', int(str(numero)[tamanoNumero - 3] + '00')
    else : valorPosicional, respuesta = 'Millares', int(str(numero)[tamanoNumero - 4] + '000')
        
    if valorPosicional[len(valorPosicional)-1] == 'a': cuanto = 'cuantas' 
    else: cuanto = 'cuantos'
    
    if numero != 1:
        objeto = objeto + 's'
    
    pregunta = 'Si ' + persona + ' tiene ' + str(numero) + ' ' + objeto + ', ' + cuanto + ' ' + valorPosicional + ' tiene?'
    return [pregunta, respuesta]