from datetime import datetime

from .excepciones import JustificacionInvalidaError

class Descarte:
    def __init__(self, justificacion, fecha_hora):
        if not justificacion.strip():
            raise CampoVacioError("La justificación del descarte no puede estar vacía.")

        self._justificacion= justificacion.strip()
        self._fecha_hora = fecha_hora

    @property
    def justificacion(self):
        return self._justificacion

    @property
    def fecha_hora(self):
        return self._fecha_hora