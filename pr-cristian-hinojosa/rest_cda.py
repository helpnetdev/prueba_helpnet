from flask import Flask
from flask_restful import Resource, Api
import requests
import datetime, random
from datetime import date, timedelta

app = Flask(__name__)
api = Api(app)

class RestCda(Resource):

    def turno_entrada(self):
        listado_horas = [7,8]
        return self.periodo_tiempo(listado_horas)

    
    def turno_salida(self):
        listado_horas = [18,19]
        return self.periodo_tiempo(listado_horas)

    def periodo_tiempo(self, listado_horas):
        tiempo = list(range (1, 59))
        hora = random.choice(listado_horas)
        minuto = random.choice(tiempo)
        segundo = random.choice(tiempo)
        if hora < 10:
            hora = str(0) + str(hora)
        if minuto < 10:
            minuto = str(0) + str(minuto)
        if segundo < 10:
            segundo = str(0) + str(segundo)
        return "{}:{}:{}".format(hora, minuto, segundo)

    def get(self):
        cda_datos = requests.get('http://desafio.helpnet.cl/cda')
        dato =  cda_datos.json()
        fecha_inicio = datetime.datetime.strptime(dato['fechaInicio'], '%Y-%m-%d')
        fecha_termino = datetime.datetime.strptime(dato['fechaFin'], '%Y-%m-%d')
        contador_dia = timedelta(days=1)
        listado_registros = []
        listado_fechas_input = []

        while fecha_inicio <= fecha_termino:
            fecha_inicio_string = str(fecha_inicio.date())
            for registro in dato['registros']:
                if  fecha_inicio_string == registro['fecha']:
                    if registro['horaEntrada']:
                        entrada = registro['horaEntrada']
                    else:
                        entrada = self.turno_entrada()
                    if registro['horaSalida']:
                        salida = registro['horaSalida']
                    else:
                        salida = self.turno_salida()
                    listado_registros.append({"fecha" : fecha_inicio_string, 
                        "horaEntrada" : entrada, 
                        'horaSalida':salida,})
                    listado_fechas_input.append(fecha_inicio_string)
                            
            if fecha_inicio_string not in listado_fechas_input:
                listado_registros.append({"fecha" : fecha_inicio_string, 
                    "horaEntrada" : self.turno_entrada(), 
                    'horaSalida':self.turno_salida(),
                    })
                listado_fechas_input.append(fecha_inicio_string)
            fecha_inicio += contador_dia
        
        dato["registros"] = listado_registros
        return dato

api.add_resource(RestCda, '/')

if __name__ == '__main__':
    app.run(debug=True)