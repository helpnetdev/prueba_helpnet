class Registro(object):
    def __init__(self, fecha, horaEntrada,horaSalida):
        self.fecha = fecha
        self.horaEntrada = horaEntrada
        self.horaSalida = horaSalida


class Asistencia(object):
    def __init__(self, id, fechaInicio,fechaFin, created=None):
        self.id = id
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin

# comment = Comment(email='leila@example.com', content='foo bar')