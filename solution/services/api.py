# Native
from datetime import datetime
from datetime import timedelta
from random import randint

# Django
from django.http import JsonResponse

# Rest
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

# Internal
from services.utils.connection import dispatcher_data_json


class FixDatesView(APIView):
    """
        Arreglas los datos de fecha inicio y fecha final.

        Author
        -------
            - Miguel Sánchez Padilla

        Last Modification
        -----------------
            - 11/09/2019
    """
    authentication_classes = ()
    permission_classes = ()
    parser_classes = (JSONParser,)

    def get(self, request):
        """
            Consulta haciendo un request al api de CDA
        """
        result = None
        response = self.catch_request_cda()

        if "data" in response:
            data = response.get('data', {})
            result = self.fix_date(data)

        if result:
            return JsonResponse(
                {'status': 'OK', 'data': result},
                status=status.HTTP_200_OK
            )

        return JsonResponse(
            {'status': 'ER'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def post(self, request):
        """
            Recibe un json para arreglar los datos.
        """
        result = None
        data = request.data

        # Tiene que ser un diccionario para entrar.
        if isinstance(data, dict):
            # Repara los datos
            result = self.fix_date(data)
        else:
            return JsonResponse(
                {'status': 'ER', 'type': 'Error del formato.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if result:
            return JsonResponse(
                {'status': 'OK', 'data': result},
                status=status.HTTP_200_OK
            )

        return JsonResponse(
            {'status': 'ER'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def fix_date(self, data):
        """
            Requisitos
            ----------
            rango de llegada 7:00 - 9:00
            rango de salida 18:00 - 20:00

            Author
            -------
                - Miguel Sánchez Padilla

            Last Modification
            -----------------
                - 11/09/2019
        """
        format_date = '%Y-%m-%d'
        fecha_inicio_string = data.get('fechaInicio')
        fecha_fin_string = data.get('fechaFin')
        registros = data.get('registros')
        registro_completo = []

        fecha_inicio = datetime.strptime(fecha_inicio_string, format_date)
        fecha_fin = datetime.strptime(fecha_fin_string, format_date)

        cantidad_dias = (fecha_fin - fecha_inicio).days

        try:
            fecha_recorrido = fecha_inicio
            # Ingresa al for donde pasara por todos los días llenando los datos que falta.
            for dias_completos in range(cantidad_dias):
                horaEntrada = ''
                horaSalida = ''

                # Si existen datos los llenara.
                for registro in registros:
                    fecha = datetime.strptime(registro.get('fecha'), format_date)

                    if fecha == fecha_recorrido:
                        horaEntrada = registro.get('horaEntrada')
                        horaSalida = registro.get('horaSalida')

                # Si no le aplicara un random a cada parte de la hora.
                if not horaEntrada:
                    hora_temp = randint(7, 9)
                    minuto_temp = randint(0, 59)
                    segundo_temp = randint(0, 59)
                    horaEntrada = f'{hora_temp}:{minuto_temp}:{segundo_temp}'

                if not horaSalida:
                    hora_tard = randint(18, 20)
                    minuto_tard = randint(0, 59)
                    segundo_tard = randint(0, 59)
                    horaSalida = f'{hora_tard}:{minuto_tard}:{segundo_tard}'

                # Creando el diccionario con los datos.
                date_dict = {
                    'fecha': fecha_recorrido.strftime(format_date),
                    'horaEntrada': horaEntrada,
                    'horaSalida': horaSalida
                }

                registro_completo.append(date_dict)
                fecha_recorrido = fecha_recorrido + timedelta(days=1)

            data.update({'registros': registro_completo})
        except Exception:
            print('Se ingreso mal el formato.')

        return data

    def catch_request_cda(self):
        """
            Request donde hara la consulta a CDA

            Author
            -------
                - Miguel Sánchez Padilla

            Last Modification
            -----------------
                - 11/09/2019
        """
        URL = 'http://desafio.helpnet.cl/cda'
        return dispatcher_data_json('GET', URL)
