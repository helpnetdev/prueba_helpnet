from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
import requests
import json
from datetime import date, timedelta, datetime
import random


def registroAsistencia(request):
    URL = 'http://desafio.helpnet.cl/cda'
    response = requests.get(URL)
    if response.status_code != 200:
        return HttpResponse('Servicio de API no disponible en este momento',status = 400)
    data = json.loads(response.content.decode('utf-8'))
    sdate = datetime.strptime(data['fechaInicio'], "%Y-%m-%d").date()
    edate = datetime.strptime(data['fechaFin'], "%Y-%m-%d").date()
    delta =  edate- sdate
    for registro in data['registros']:
        if registro['horaEntrada'] == '':
            entrada = datetime.now().replace(hour=random.randint(7,8),minute=random.randint(0,59))
            registro['horaEntrada'] = str(entrada.hour) + ':' + str(entrada.minute) + ':' + str(entrada.second)
        if registro['horaSalida'] == '':
                salida = datetime.now().replace(hour=random.randint(18,19),minute=random.randint(0,59))
                registro['horaSalida'] = str(salida.hour) + ':' + str(salida.minute) + ':' + str(salida.second)
    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        entrada = datetime.now().replace(hour=random.randint(7,8),minute=random.randint(0,59))
        salida = datetime.now().replace(hour=random.randint(18,19),minute=random.randint(0,59))
        if (i<len(data['registros'])):
            if datetime.strptime(data['registros'][i]['fecha'], "%Y-%m-%d").date() != day:
                data['registros'].insert(i, {"fecha": day.strftime("%Y-%m-%d"),"horaEntrada": str(entrada.hour) + ':' + str(entrada.minute) + ':' + str(entrada.second),"horaSalida": str(salida.hour) + ':' + str(salida.minute) + ':' + str(salida.second)})

        else:
            data['registros'].append({"fecha": day.strftime("%Y-%m-%d"),"horaEntrada": str(entrada.hour) + ':' + str(entrada.minute) + ':' + str(entrada.second),"horaSalida": str(salida.hour) + ':' + str(salida.minute) + ':' + str(salida.second)})

    return JsonResponse(data, safe=False)