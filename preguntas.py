# -*- coding: utf-8 -*-
from random import randint

#Numero Antes
def numeroAntes(minn, maxn):
    numero = randint(minn,maxn)
    pregunta = '¿Qué número está antes del ' + str(numero) + '?'
    respuesta = numero - 1
    return [pregunta, respuesta, None]

#Numero Despues
def numeroDespues(minn, maxn):
    numero = randint(minn,maxn)
    pregunta = '¿Qué número esta después del número ' + str(numero) + '?'
    respuesta = numero + 1
    return [pregunta, respuesta, None]
    
#Numero Entre
def numeroEntre(minn, maxn):
    numero1 = randint(minn,maxn)
    numero2 = numero1 + 2
    pregunta = '¿Qué número está entre el número ' + str(numero1) + ' y el ' + str(numero2) + '?'
    respuesta = numero1 + 1
    return [pregunta, respuesta, None]

#Preguntas valor posicional
def valorPosicional(persona, objeto, minn, maxn):
    numero = randint(minn,maxn)
    
    tamanoNumero = len(str(numero))
    unidad = randint(1, tamanoNumero)
    if unidad < 2: valorPosicional, respuesta = 'Unidades' , int(str(numero)[tamanoNumero - 1])
    elif unidad < 3: valorPosicional, respuesta = 'Decenas', int(str(numero)[tamanoNumero - 2])# + '0')
    elif unidad < 4: valorPosicional, respuesta = 'Centenas', int(str(numero)[tamanoNumero - 3])# + '00')
    else : valorPosicional, respuesta = 'Millares', int(str(numero)[tamanoNumero - 4])# + '000')
        
    if valorPosicional == 'Millares': cuanto = 'cuantos' 
    else: cuanto = 'cuantas'
    
    if numero != 1:
        objeto = objeto + 's'
    
    listaModelosPreguntas = [
        'Si ' + persona + ' tiene ' + str(numero) + ' ' + objeto + ', ' + cuanto + ' ' + valorPosicional + ' de ' + objeto + ' tiene?',
        'Si compro ' + str(numero) + ' ' + objeto + ', ' + cuanto + ' ' + valorPosicional + ' de ' + objeto + ' compre?',
        'Si regalo ' + str(numero) + ' ' + objeto + ', ' + cuanto + ' ' + valorPosicional + ' de ' + objeto + ' regale?'
    ]
    indiceModeloPregunta = randint(0,len(listaModelosPreguntas) - 1)
    pregunta = listaModelosPreguntas[indiceModeloPregunta]
    
    imagen = "/static/svgs/" + objeto + ".svg"
    return [pregunta, respuesta, imagen]

# Preguntas Restas
def resta(persona, comida, minn, maxn):
    # Si <persona> tiene <numero> <comida> y se come <numero>, cuanta(s) <comida> le queda(n)?
    numero1 = randint(minn,maxn)
    numero2 = randint(1,numero1)
    respuesta = numero1-numero2
    imagen = "/static/svgs/" + comida + ".svg"
    
    if comida[len(comida)-1] == 'a': cuanto = 'cuantas' 
    else: cuanto = 'cuantos'
    
    if numero1 > 1: plural = 's'
    else: plural = ''

    listaModelosPreguntas = [
        'Si '+persona+' tiene '+str(numero1)+' '+comida+plural + ' y se come '+str(numero2)+', '+cuanto+' '+comida+plural+' le quedan?',
        'Si '+persona+' compra '+str(numero1)+' '+comida+plural + ' y luego vende '+str(numero2)+', '+cuanto+' '+comida+plural+' le quedan?',
        'Tengo '+str(numero1)+' '+comida+plural + ' y le regalo '+str(numero2)+' a '+persona+ ', ' +cuanto+' '+comida+plural+' me quedan?'
    ]
    indiceModeloPregunta = randint(0,len(listaModelosPreguntas) - 1)
    pregunta = listaModelosPreguntas[indiceModeloPregunta]

    return [pregunta,respuesta,imagen]
    
#Preguntas Sumas
def suma(persona1, persona2, accion, accionPasado, minn, maxn):
    # <persona> <accion> <numero> veces, <persona2> <accion> <numero> veces mas que <persona>, cuantas veces <accionpasado> <persona2>?
    imagen = "/static/svgs/" + accion + ".svg"
    numero1 = randint(minn,maxn)
    numero2 = randint(1,maxn)
    
    respuesta = numero1 + numero2
    
    pregunta = 'Si ' + persona1 + ' ' + accion + ' ' + str(numero1) + ' kilometros y ' + persona2 + ' ' + str(numero2) + ' quien de los dos ' + accionPasado + ' mas?'
    
    return [pregunta,respuesta,imagen]

#Preguntas Multiplicaciones
def multiplicacion(persona, objeto, minn, maxn):
    imagen = "/static/svgs/" + objeto + ".svg"
    numero1 = randint(1,maxn)
    numero2 = randint(minn, maxn)
    
    if numero1 > 1: plural1 = 's'
    else: plural1 = ''
    
    if numero2 > 1: plural2 = 's'
    else: plural2 = ''
    
    respuesta = numero1 * numero2
    
    listaModelosPreguntas = [
        persona + 'tiene ' + str(numero1) + ' bolsas cada una con ' + str(numero2) + ' ' + objeto + plural2 + ' dentro, cuantas ' + objeto + plural2 + ' compro ' + persona + '?',
        'Si en una camioneta llevo ' + str(numero1) + ' cajas con ' + str(numero2) + ' ' + objeto + plural2 + ' cada una, ' + ' qué número de ' + objeto + plural2 + ' llevo?',
        persona + ' recoge ' + str(numero1) + ' ' + objeto + plural1 + ' cada dia, cúal es el número de ' + objeto + plural1 + ' que tendrá ' + persona + ' después de ' + str(numero2) + ' dias?'
    ]
    indiceModeloPregunta = randint(0,len(listaModelosPreguntas) - 1)
    pregunta = listaModelosPreguntas[indiceModeloPregunta]
    
    return [pregunta,respuesta,imagen]
    
#Preguntas posicion numerica
# def posicionNumericaA(persona,  maxn):
#     numero1 = randint(1,maxn)
    
#     if randint(1, 2) == 1: antesDespues, respuesta = 'antes', numero1 - 1 
#     else: antesDespues, respuesta = 'despues ', numero1 + 1
    
#     pregunta = persona + ' tiene el turno ' + str(numero1) + ' para jugar con el balon, que turno tiene la persona ' + antesDespues + ' que ' + persona + '?'
#     return [pregunta, respuesta]

# def posicionNumericaB(persona1, persona2, persona3):
#     numero = 0
#     if randint(1, 2) == 1:  
#         numero = randint(1,10)
#         antesDespues, respuesta = numero + 2, numero + 1
#     else: 
#         numero = randint(3,12) 
#         antesDespues, respuesta = numero - 2, numero - 1
    
#     pregunta = 'Un tren que sale a cada hora, el cual ' + persona1 + ' lo toma a las ' + str(numero) + ' y ' + persona2 + ' toma el tren a las ' + str(antesDespues) + ' a que hora tomo el tren ' + persona3 + ' si salio entre ' + persona1 + ' y ' + persona2 +'?' 
#     return [pregunta, respuesta]

#Preguntas conjuntos
def conjuntosIguales(animal1, animal2):
    
    totalConjuntoA = randint(1, 5)
    totalConjuntoB = randint(1, 5)
    
    pregunta = 'Hay dos manadas de animales, escúchalos y escribe si el número de animales en cada manada es diferente o es igual.'
    
    if totalConjuntoA != totalConjuntoB:
        respuesta = 'diferente'
    else:
        respuesta = 'igual'
        
    imagen = "/static/svgs/" + animal1 + ".svg"
    
    return [pregunta, respuesta, imagen , animal1, animal2, totalConjuntoA, totalConjuntoB]

def conjuntoMayor(animal1, animal2):
    
    totalConjuntoA = randint(1, 5)
    totalConjuntoB = randint(1, 5)
    while totalConjuntoA == totalConjuntoB:
        totalConjuntoB = randint(1, 5)

    pregunta = 'Hay dos manadas de animales, escúchalos y escribe cual es el nombre del animal con mayor número'
    
    if totalConjuntoA > totalConjuntoB:
        respuesta = str(animal1)
    else:
        respuesta = str(animal2)
    
    imagen = "/static/svgs/" + animal1 + ".svg"
    
    return [pregunta, respuesta, imagen , animal1, animal2, totalConjuntoA, totalConjuntoB]

def conjuntoMenor(animal1, animal2):
    
    totalConjuntoA = randint(1, 5)
    totalConjuntoB = randint(1, 5)
    while totalConjuntoA == totalConjuntoB:
        totalConjuntoB = randint(1, 5)
    
    pregunta = 'Hay dos manadas de animales, escúchalos y escribe cual es el nombre del animal con menor número'
    
    if totalConjuntoA < totalConjuntoB:
        respuesta = str(animal1)
    else:
        respuesta = str(animal2)
    
    imagen = "/static/svgs/" + animal1 + ".svg"
    
    return [pregunta, respuesta, imagen , animal1, animal2, totalConjuntoA, totalConjuntoB]

def contarSonidos(animal1, animal2):
    
    totalConjuntoA = randint(1, 5)
    totalConjuntoB = randint(1, 5)
    
    pregunta = 'Dos animales cantan sin parar, cuenta cuantas veces cantan en total?'
    
    respuesta = totalConjuntoA + totalConjuntoB
    
    imagen = "/static/svgs/" + animal1 + ".svg"
    
    return [pregunta, respuesta, imagen , animal1, animal2, totalConjuntoA, totalConjuntoB]