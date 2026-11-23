from datetime import datetime

from dominio.excepciones import (AutorNoValidoError, CampoVacioError, OperacionNoPermitidaError)

class Aviso:
    def __init__(self, reportante, ubicacion, tipo_situacion, gravedad_estimada, descripcion, fecha_hora):
        if not ubicacion.strip():
            raise CampoVacioError("La ubicación del aviso no puede estar vacía.")
        if not descripcion.strip():
            raise CampoVacioError("La descripción inicial del aviso no puede estar vacía.")

        self._reportante = reportante
        self._ubicacion = ubicacion.strip()
        self._tipo_situacion = tipo_situacion
        self._gravedad_estimada = gravedad_estimada
        self._descripcion = descripcion.strip()
        self._fecha_hora = fecha_hora
        self._estado = EstadoAviso.PENDIENTE
        self._notas = []
        self._descarte = None

    @property
    def reportante(self):
        return self._reportante

    @property
    def ubicacion(self):
        return self._ubicacion

    @property
    def tipo_situacion(self):
        return self._tipo_situacion

    @property
    def gravedad_estimada(self):
        return self._gravedad_estimada

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def fecha_hora_registro(self):
        return self._fecha_hora_registro

    @property
    def estado(self):
        return self._estado

    @property
    def notas(self):
        return list(self._notas)

    @property
    def descarte(self):
        return self._descarte

    def pertenece_a(self, reportante):
        return self._reportante == reportante

    