# Desafío: Asistencia de Personal con Errores

El desafío consiste en lo siguiente:

-	Existe un servicio REST que llamaremos Consultor de Asistencia CDA.
	-	El servicio responde a la consulta de un registro de asistencia para una persona. Las fechas se encuentran en un rango definido por dos valores: fechaInicio y fechaFin.
	-	Cada fecha generada corresponde a un día dentro del rango mencionado anteriormente e indica la hora de entrada y salida de la persona.
	-	El servicio no entrega todas las fechas o registros de entrada / salida dentro del periodo, omite algunas de forma aleatoria.
	-	El objetivo de este ejercicio es completar con las fechas y registros que faltan.

Este es un ejemplo de la respuesta que entrega este servicio:

```json
{  
   "id":"581219199",
   "fechaInicio":"2019-03-09",
   "fechaFin":"2019-03-26",
   "registros":[  
      {  
         "fecha":"2019-03-09",
         "horaEntrada":"",
         "horaSalida":""
      },
      {  
         "fecha":"2019-03-14",
         "horaEntrada":"",
         "horaSalida":""
      },
      {  
         "fecha":"2019-03-16",
         "horaEntrada":"08:19:32",
         "horaSalida":""
      },
      {  
         "fecha":"2019-03-19",
         "horaEntrada":"07:51:13",
         "horaSalida":""
      },
      {  
         "fecha":"2019-03-24",
         "horaEntrada":"",
         "horaSalida":"19:48:39"
      }
   ]
}
```

Acá se puede apreciar que el servicio generó fechas entre el 09 de marzo de 2019 y el 26 de marzo de 2019. Sólo se generaron 5 fechas en este caso. 
De acuerdo a esto, faltarían 12 fechas (10,11,12,13,15,17,18,20,21,22,23,25) además de los registros de entrada y salida correspondiente.

Para generar los horarios se deben utilizar los siguientes parametros: el horario de llegada debe ser entre 7:00 y 9:00, el de salida entre 18:00 y 20:00 hrs.




Una versión del CDA se encuentra en :
http://desafio.helpnet.cl/cda

El desafío puede ser resuelto de las siguiente manera:


## SOLUCIÓN 1: 
	Crear un programa que recibe, a través de la entrada estándar, un archivo en formato Json con la estructura de la respuesta de servicio (como el ejemplo de arriba) y que entrega a través de la salida estándar, como respuesta, un archivo Json con las fechas faltantes.
Ejemplo:
	Se entrega un archivo con este contenido:
	
```json
{  
   "id":"581219199",
   "fechaInicio":"2019-03-09",
   "fechaFin":"2019-03-26",
   "registros":[  
      {  
         "fecha":"2019-03-09",
         "horaEntrada":"",
         "horaSalida":""
      },
      {  
         "fecha":"2019-03-14",
         "horaEntrada":"",
         "horaSalida":""
      },
      {  
         "fecha":"2019-03-16",
         "horaEntrada":"08:19:32",
         "horaSalida":""
      },
      {  
         "fecha":"2019-03-19",
         "horaEntrada":"07:51:13",
         "horaSalida":""
      },
      {  
         "fecha":"2019-03-24",
         "horaEntrada":"",
         "horaSalida":"19:48:39"
      }
   ]
}
```

El programa debe responder con archivo con este contenido:
	
```json
{  
   "id":"581219199",
   "fechaInicio":"2019-03-09",
   "fechaFin":"2019-03-26",
   "registros":[  
      {  
         "fecha":"2019-03-09",
         "horaEntrada":"07:32:12",
         "horaSalida":"18:47:29"
      },
	  {  
         "fecha":"2019-03-10",
         "horaEntrada":"08:11:56",
         "horaSalida":"19:13:56"
      },
	  {  
         "fecha":"2019-03-11",
         "horaEntrada":"08:15:02",
         "horaSalida":"18:51:12"
      },
	  {  
         "fecha":"2019-03-12",
         "horaEntrada":"08:45:17",
         "horaSalida":"19:02:32"
      },
	  {  
         "fecha":"2019-03-13",
         "horaEntrada":"07:49:34",
         "horaSalida":"18:35:16"
      },
      {  
         "fecha":"2019-03-14",
         "horaEntrada":"07:39:09",
         "horaSalida":"19:42:36"
      },
	  {  
         "fecha":"2019-03-15",
         "horaEntrada":"08:36:28",
         "horaSalida":"18:02:45"
      },
      {  
         "fecha":"2019-03-16",
         "horaEntrada":"08:19:32",
         "horaSalida":"19:54:58"
      },
	  {  
         "fecha":"2019-03-17",
         "horaEntrada":"07:19:32",
         "horaSalida":"18:41:27"
      },
	  {  
         "fecha":"2019-03-18",
         "horaEntrada":"07:19:32",
         "horaSalida":"18:03:51"
      },
      {  
         "fecha":"2019-03-19",
         "horaEntrada":"07:51:13",
         "horaSalida":"18:21:47"
      },
	  {  
         "fecha":"2019-03-20",
         "horaEntrada":"07:16:31",
         "horaSalida":"18:07:59"
      },
	  {  
         "fecha":"2019-03-21",
         "horaEntrada":"08:19:32",
         "horaSalida":"19:43:04"
      },
	  {  
         "fecha":"2019-03-22",
         "horaEntrada":"08:19:32",
         "horaSalida":"19:33:51"
      },
	  {  
         "fecha":"2019-03-23",
         "horaEntrada":"08:19:32",
         "horaSalida":"19:11:00"
      },
	  {  
         "fecha":"2019-03-24",
         "horaEntrada":"08:19:32",
         "horaSalida":"19:48:39"
      },
      {  
         "fecha":"2019-03-25",
         "horaEntrada":"08:19:32",
         "horaSalida":"19:48:39"
      },
	  {  
         "fecha":"2019-03-26",
         "horaEntrada":"08:19:32",
         "horaSalida":"19:48:39"
      }
   ]
}
```
 
El programa se debe ejecutar de la siguiente manera:
	$ mi_solucion < nombre_archivo_entrada > nombre_archivo_salida


## Nivel 3:

Implementar un nuevo servicio REST. Este servicio REST debe invocar al servicio CDA y entregar la respuesta en formato JSON con las fechas recibidas y las fechas faltantes.
Ejemplo de la respuesta que debería entregar:

	
```json
{  
   "id":"581219199",
   "fechaInicio":"2019-03-09",
   "fechaFin":"2019-03-26",
   "registros":[  
      {  
         "fecha":"2019-03-09",
         "horaEntrada":"07:32:12",
         "horaSalida":"18:47:29"
      },
	  {  
         "fecha":"2019-03-10",
         "horaEntrada":"08:11:56",
         "horaSalida":"19:13:56"
      },
	  {  
         "fecha":"2019-03-11",
         "horaEntrada":"08:15:02",
         "horaSalida":"18:51:12"
      },
	  {  
         "fecha":"2019-03-12",
         "horaEntrada":"08:45:17",
         "horaSalida":"19:02:32"
      },
	  {  
         "fecha":"2019-03-13",
         "horaEntrada":"07:49:34",
         "horaSalida":"18:35:16"
      },
      {  
         "fecha":"2019-03-14",
         "horaEntrada":"07:39:09",
         "horaSalida":"19:42:36"
      },
	  {  
         "fecha":"2019-03-15",
         "horaEntrada":"08:36:28",
         "horaSalida":"18:02:45"
      },
      {  
         "fecha":"2019-03-16",
         "horaEntrada":"08:19:32",
         "horaSalida":"19:54:58"
      },
	  {  
         "fecha":"2019-03-17",
         "horaEntrada":"07:19:32",
         "horaSalida":"18:41:27"
      },
	  {  
         "fecha":"2019-03-18",
         "horaEntrada":"07:19:32",
         "horaSalida":"18:03:51"
      },
      {  
         "fecha":"2019-03-19",
         "horaEntrada":"07:51:13",
         "horaSalida":"18:21:47"
      },
	  {  
         "fecha":"2019-03-20",
         "horaEntrada":"07:16:31",
         "horaSalida":"18:07:59"
      },
	  {  
         "fecha":"2019-03-21",
         "horaEntrada":"08:19:32",
         "horaSalida":"19:43:04"
      },
	  {  
         "fecha":"2019-03-22",
         "horaEntrada":"08:19:32",
         "horaSalida":"19:33:51"
      },
	  {  
         "fecha":"2019-03-23",
         "horaEntrada":"08:19:32",
         "horaSalida":"19:11:00"
      },
	  {  
         "fecha":"2019-03-24",
         "horaEntrada":"08:19:32",
         "horaSalida":"19:48:39"
      },
      {  
         "fecha":"2019-03-25",
         "horaEntrada":"08:19:32",
         "horaSalida":"19:48:39"
      },
	  {  
         "fecha":"2019-03-26",
         "horaEntrada":"08:19:32",
         "horaSalida":"19:48:39"
      }
   ]
}
```

REQUISITOS:
-	Se pueden implementar las soluciones en cualquier lenguaje y framework. Aunque recomendamos usar: Java(con o sin Spring Boot), Go o Python.
-	La solución debe ser enviada vía un pull request a este repositorio.
-	La solución debe contener un README.md con las instrucciones para compilar e instalar.
-	Puedes implementar cualquiera de las soluciones, no es necesario implementar todas.
-	Junto con la solución debes entregar un archivo con la entrada y con la salida en formato JSON.

NOTA:
Todos los pull request serán rechazados, esto no quiere decir que ha sido rechazada la solución, sino que es una forma de que otros postulantes no copien tu código.
