from dominio.excepciones import DatoInvalidoError, CampoVacioError

class ReportanteInstitucional:
    def __init__(self, id, nombre, institucion):
        if id <= 0:
            raise DatoInvalidoError("El identificador del reportante debe ser un entero positivo.")
        if not nombre.strip():
            raise CampoVacioError("El nombre del reportante no puede estar vacío.")
        if not institucion.strip():
            raise CampoVacioError("La institución del reportante no puede estar vacía.")

        self._id = id
        self._nombre = nombre.strip()
        self._institucion = institucion.strip()

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @property
    def institucion(self):
        return self._institucion

    def __eq__(self, otro):
        return self._id == otro._id