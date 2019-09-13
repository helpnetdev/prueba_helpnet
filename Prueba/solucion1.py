import json
from datetime import date, timedelta, datetime
import random

nueva_data  = {
    'id': '',
    'fechaInicio': '',
    'fechaFin': '',
    'registros': None
}

print('cda.json')

with open('cda.json','r') as json_file:
    data = json.load(json_file)
    nueva_data['id'] = data['id']
    nueva_data['fechaInicio'] = data['fechaInicio']
    nueva_data['fechaFin'] = data['fechaFin']
    nueva_data['registros'] = data['registros']


sdate = datetime.strptime(nueva_data['fechaInicio'], "%Y-%m-%d").date()
edate = datetime.strptime(nueva_data['fechaFin'], "%Y-%m-%d").date()
delta =  edate- sdate

for registro in nueva_data['registros']:
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
    if (i<len(nueva_data['registros'])):
        if datetime.strptime(nueva_data['registros'][i]['fecha'], "%Y-%m-%d").date() != day:
            nueva_data['registros'].insert(i, {"fecha": day.strftime("%Y-%m-%d"),"horaEntrada": str(entrada.hour) + ':' + str(entrada.minute) + ':' + str(entrada.second),"horaSalida": str(salida.hour) + ':' + str(salida.minute) + ':' + str(salida.second)})

    else:
        nueva_data['registros'].append({"fecha": day.strftime("%Y-%m-%d"),"horaEntrada": str(entrada.hour) + ':' + str(entrada.minute) + ':' + str(entrada.second),"horaSalida": str(salida.hour) + ':' + str(salida.minute) + ':' + str(salida.second)})




with open('my_cda.json', 'w+') as outfile:
    json.dump(nueva_data, outfile)


print('my_cda.json')
