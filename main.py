from flask import Flask
from flask import jsonify
from datetime import date, timedelta
import random
import requests
import json
from collections import OrderedDict 

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

#Horario
#el horario de llegada debe ser entre 7:00 y 9:00, el de salida entre 18:00 y 20:00 hrs.
HORARIO_ENTRADA = (7, 9)
HORARIO_SALIDA = (18 ,20)

#devolver una hora según requerimiento
def generar_hora(hinicio, hfin):
    max_delta = timedelta(hours=hfin) - timedelta(hours=hinicio)
    hora = timedelta(hours=hinicio) + timedelta(seconds=random.randint(1, max_delta.seconds))
    str_hora = str(hora)
    hora, minutos, segundos = str_hora.split(':')
    return '{:02}:{:02}:{:02}'.format(int(hora), int(minutos), int(segundos))
    


#request al servicio cda
def consultar_cda():
    cda = requests.get('http://desafio.helpnet.cl/cda')
    if cda.status_code == 200:
        with open('input.json','w') as input_data: #grabar salida cda en archivo
            input_data.write( cda.text) 
        return cda
    else:
        return False
    
#procesar la respuesta del servicio para completar los días y horas faltantes
def procesar_data( cda_resp=''):
    try:
        cda_parsed = cda_resp.json()
        id = cda_parsed['id']
        fechaInicio = cda_parsed['fechaInicio']
        fechaFin = cda_parsed['fechaFin']
        registros = cda_parsed['registros']
        dias = date.fromisoformat(fechaFin) - date.fromisoformat(fechaInicio)
        salida = dict()
        #usar la fecha como key del diccionario
        for reg in registros:
            horaEntrada = reg['horaEntrada'] if reg['horaEntrada'] != '' else generar_hora(*HORARIO_ENTRADA)
            horaSalida = reg['horaSalida'] if reg['horaSalida'] != '' else generar_hora(*HORARIO_SALIDA)
            salida[reg['fecha']] = (horaEntrada,horaSalida)
        

        for i in range( dias.days + 1):
           fecha = str( date.fromisoformat(fechaInicio) + timedelta(days=i) ) 
           if( not fecha  in salida  ):
               salida[fecha] = (generar_hora(*HORARIO_ENTRADA), generar_hora(*HORARIO_SALIDA))
        
        #ordenar por fecha, preparar salida
        lista_horarios = list()
        for key in sorted(salida.keys()):
            lista_horarios.append({'fecha':key, 'horaEntrada': salida[key][0], 'horaSalida': salida[key][1] })
        
        #grabar salida en archivo
        with open('output.json','w') as output_data: #grabar salida retorno en archivo
            output_data.write( json.dumps({'id': id, 'fechaInicio': fechaInicio, 'fechaFin': fechaFin, 'registros': lista_horarios}))

        #agregar cabecera y retornar
        return jsonify({'id': id, 'fechaInicio': fechaInicio, 'fechaFin': fechaFin, 'registros': lista_horarios})
    except ValueError:
        return False


#API para responder con la salida completada de CDA
@app.route('/')
def nivel3():
    cda_resp = consultar_cda()
    if( cda_resp):
        cda_parsed = procesar_data( cda_resp)
        if( cda_parsed):
            return cda_parsed
        else:
            return 'No se pudo procesar los datos de CDA'
    else:
        return 'Error al consultar servicio Cda'
