class DatoInvalidoError(Exception):
    pass


class CampoVacioError(DatoInvalidoError):
    pass


class OperacionNoPermitidaError(Exception):
    pass


class AutorNoValidoError(OperacionNoPermitidaError):
    pass