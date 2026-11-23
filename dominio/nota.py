from datetime import datetime

from dominio.excepciones import DatoInvalidoError

class Nota:
    def __init__(self, autor, texto, fecha_hora):
        if not texto.strip():
            raise DatoInvalidoError("El texto de la nota no puede estar vacío.")

        self._autor = autor
        self._texto = texto.strip()
        self._fecha_hora = fecha_hora

    @property
    def autor(self):
        return self._autor

    @property
    def texto(self):
        return self._texto

    @property
    def fecha_hora(self):
        return self._fecha_hora